from flask import jsonify, request
from datetime import datetime
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from stats.advanced import get_advanced_stats
from core.data_utils import get_data
import json, os, hashlib

def register_analyse_custom_routes(app, analyse_func):
    @app.route('/QTSBE/analyse_custom', methods=['POST'])
    def analyse_custom_endpoint():
        ts_format = "%Y-%m-%d %H:%M:%S"
        pair = request.args.get('pair')
        start_ts = request.args.get('start_ts')
        end_ts = request.args.get('end_ts')
        multi_positions = request.args.get('multi_positions')
        details = request.args.get('details')
        position_type = request.args.get('position_type', 'long')
        strategy_code = request.json.get('strategy_code')

        if not pair or not strategy_code: return jsonify({"error": "missing params"}), 400
        
        try:
            import types
            mod = types.ModuleType('custom_strategy')
            exec(strategy_code, mod.__dict__)
            strat = {"buy_signal": mod.buy_signal, "sell_signal": mod.sell_signal, "Indicators": mod.Indicators}

            if start_ts: start_ts = datetime.strptime(start_ts.strip("'").strip('"'), ts_format)
            if end_ts: end_ts = datetime.strptime(end_ts.strip("'").strip('"'), ts_format)

            data = get_data(pair)
            data = [(row[0] + " 00:00:00" if len(row[0]) == 10 else row[0], *row[1:]) for row in data]
            result = analyse_func(data, start_ts, end_ts, multi_positions == 'True', strat, position_type)

            res = {
                "pair": pair, "strategy": "custom", "position_type": str(position_type),
                "data": data if details == "True" else [],
                "result": (result.indicators if details == "True" else [], result.positions, result.current_positions),
                "stats": {"drawdown": get_drawdowns_stats(result), "positions": get_position_stats(result), "advanced": get_advanced_stats(result)}
            }
            return jsonify(res)
        except Exception as e:
            return jsonify({"error": str(e)}), 400