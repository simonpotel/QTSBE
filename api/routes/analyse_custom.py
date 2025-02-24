from flask import jsonify, request
from datetime import datetime
from loguru import logger
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from core.file_utils import get_file_data
import json
import os
from collections import deque, defaultdict
import hashlib

CACHE_DIR = "logs/api"
MAX_CACHE_ENTRIES = 500

class CustomAnalysisCache:
    def __init__(self):
        self.cache_file = os.path.join(CACHE_DIR, "customnAnalysisCache.json")
        self.entries = {}  
        self._load_cache()

    def _load_cache(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    loaded_entries = json.load(f)
                    self.entries = {}
                    for key, entry in loaded_entries.items():
                        entry_copy = entry.copy()
                        entry_copy['pairs'] = set(entry_copy['pairs'])
                        self.entries[key] = entry_copy
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
                self.entries = {}
        else:
            self.entries = {}

    def _save_cache(self):
        try:
            sorted_entries = dict(sorted(
                self.entries.items(),
                key=lambda x: x[1]['cumulative_return'],
                reverse=True
            )[:MAX_CACHE_ENTRIES])
            
            serializable_entries = {}
            for key, entry in sorted_entries.items():
                entry_copy = entry.copy()
                entry_copy['pairs'] = list(entry_copy['pairs'])
                serializable_entries[key] = entry_copy
            
            with open(self.cache_file, 'w') as f:
                json.dump(serializable_entries, f)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    def add_entry(self, strategy_code, pair, stats, timestamp):
        strategy_hash = hashlib.md5(strategy_code.encode()).hexdigest()
        
        new_stats = {
            'positions': {
                'average_ratio': stats['positions'].get('average_ratio', 1.0),
                'final_cumulative_ratio': stats['positions'].get('final_cumulative_ratio', 1.0),
                'average_position_duration': stats['positions'].get('average_position_duration', 0),
            },
            'drawdown': {
                'max_drawdown': stats['drawdown'].get('max_drawdown', 0),
                'average_drawdown': stats['drawdown'].get('average_drawdown', 0),
            }
        }

        if strategy_hash in self.entries:
            entry = self.entries[strategy_hash]
            entry['last_update'] = timestamp
            entry['pairs'].add(pair)
            
            n = len(entry['pairs'])
            for stat_type in ['positions', 'drawdown']:
                for key in new_stats[stat_type]:
                    old_value = entry['stats'][stat_type][key]
                    new_value = new_stats[stat_type][key]
                    entry['stats'][stat_type][key] = ((n-1) * old_value + new_value) / n
            
            new_cumulative = stats['positions'].get('final_cumulative_ratio', 1.0)
            if new_cumulative > entry['cumulative_return']:
                entry['cumulative_return'] = new_cumulative
                entry['best_pair'] = pair
        else:
            self.entries[strategy_hash] = {
                'first_seen': timestamp,
                'last_update': timestamp,
                'strategy_hash': strategy_hash,
                'pairs': {pair},
                'best_pair': pair,
                'cumulative_return': stats['positions'].get('final_cumulative_ratio', 1.0),
                'stats': new_stats,
                'strategy_code': strategy_code
            }
        
        self._save_cache()

cache = CustomAnalysisCache()

def register_analyse_custom_routes(app, analyse_func):
    @app.route('/QTSBE/analyse_custom', methods=['POST'])
    def analyse_custom_endpoint():
        ts_format = "%Y-%m-%d %H:%M:%S"
        
        pair = request.args.get('pair')
        start_ts = request.args.get('start_ts')
        end_ts = request.args.get('end_ts')
        multi_positions = request.args.get('multi_positions')
        details = request.args.get('details')
        strategy_code = request.json.get('strategy_code')

        if not pair or not strategy_code:
            return jsonify({"error": "pair and strategy_code are required"}), 400

        try:
            import types
            custom_module = types.ModuleType('custom_strategy')
            exec(strategy_code, custom_module.__dict__)
            
            custom_strategy = {
                "buy_signal": custom_module.buy_signal,
                "sell_signal": custom_module.sell_signal,
                "Indicators": custom_module.Indicators
            }

            if start_ts:
                start_ts = datetime.strptime(start_ts.strip("'").strip('"'), ts_format)
            if end_ts:
                end_ts = datetime.strptime(end_ts.strip("'").strip('"'), ts_format)

            data = get_file_data(pair)
            data = [(row[0] + " 00:00:00" if len(row[0]) == 10 else row[0], *row[1:]) for row in data]

            result = analyse_func(data, start_ts, end_ts, multi_positions, custom_strategy)

            stats = {
                "drawdown": get_drawdowns_stats(result),
                "positions": get_position_stats(result)
            }

            response_data = {
                "pair": pair,
                "strategy": "custom",
                "data": data if details == "True" else [],
                "result": (
                    result.indicators if details == "True" else [],
                    result.positions,
                    result.current_positions
                ),
                "stats": stats
            }

            cache.add_entry(
                strategy_code=strategy_code,
                pair=pair,
                stats=stats,
                timestamp=datetime.now().strftime(ts_format)
            )

            logger.info(f"Custom analyse request - pair: {pair} | start_ts: {start_ts} | end_ts: {end_ts} | multi_positions: {multi_positions} | details: {details}")
            return jsonify(response_data)

        except Exception as e:
            error_msg = f"Error in custom strategy execution: {str(e)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 400 