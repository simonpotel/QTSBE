from flask import jsonify, request
from datetime import datetime
from loguru import logger
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from core.file_utils import get_file_data
from concurrent.futures import ThreadPoolExecutor, as_completed

def register_scan_routes(app, strategies, analyse_func):
    @app.route('/QTSBE/scan')
    def scan_endpoint():
        ts_format = "%Y-%m-%d %H:%M:%S"
        
        pairs = request.args.get('pairs')
        strategy = request.args.get('strategy')
        start_ts = request.args.get('start_ts')
        end_ts = request.args.get('end_ts')
        multi_positions = request.args.get('multi_positions')
        position_type = request.args.get('position_type', 'long')
        concurrency = request.args.get('concurrency', 5)

        try:
            concurrency = int(concurrency)
            if concurrency <= 0:
                concurrency = 1
        except Exception:
            concurrency = 5

        if not pairs or not strategy:
            return jsonify({"error": "pairs and strategy parameters are required"}), 400

        if position_type not in ['long', 'short']:
            return jsonify({"error": "position_type must be either 'long' or 'short'"}), 400

        try:
            pairs_list = pairs.split(',')
            pairs_list = [pair.strip() for pair in pairs_list]
        except Exception as e:
            return jsonify({"error": "pairs must be a comma-separated list"}), 400

        if start_ts:
            start_ts = datetime.strptime(start_ts.strip("'").strip('"'), ts_format)
        if end_ts:
            end_ts = datetime.strptime(end_ts.strip("'").strip('"'), ts_format)

        multi_positions = bool(multi_positions) and (lambda s: s.lower() in {'true'})(multi_positions)

        def analyse_single_pair(pair):
            data = get_file_data(pair)
            if not data:
                return {
                    "pair": pair,
                    "error": f"No data found for pair {pair}"
                }

            data = [(
                (str(row[0]) + " 00:00:00" if isinstance(row[0], str) and len(row[0]) == 10 
                else str(row[0]) if isinstance(row[0], (int, float)) 
                else row[0]),
                float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])
            ) for row in data]

            try:
                result = analyse_func(data, start_ts, end_ts, multi_positions, strategies[strategy], position_type)
                return {
                    "pair": pair,
                    "strategy": strategy,
                    "position_type": position_type,
                    "result": (
                        [], # we dont care about indicators
                        result.positions,
                        result.current_positions
                    ),
                    "stats": {
                        "drawdown": get_drawdowns_stats(result),
                        "positions": get_position_stats(result)
                    }
                }
            except Exception as e:
                return {
                    "pair": pair,
                    "error": f"Analysis failed for pair {pair}: {str(e)}"
                }

        results_dict = {}
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            future_to_pair = {executor.submit(analyse_single_pair, pair): pair for pair in pairs_list}
            for future in as_completed(future_to_pair):
                pair = future_to_pair[future]
                try:
                    results_dict[pair] = future.result()
                except Exception as exc:
                    results_dict[pair] = {"pair": pair, "error": str(exc)}

        results = [results_dict[pair] for pair in pairs_list]

        # Aggregate statistics
        def flatten_dict(d, parent_key="", sep="."):
            items = {}
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.update(flatten_dict(v, new_key, sep=sep))
                else:
                    items[new_key] = v
            return items

        field_values = {}
        for res in results:
            if "error" in res:
                continue
            flat_stats = flatten_dict(res.get("stats", {}))
            for field, value in flat_stats.items():
                if isinstance(value, (int, float)):
                    field_values.setdefault(field, []).append((res["pair"], value))

        aggregate = {}
        for field, pair_values in field_values.items():
            pair_values_sorted = sorted(pair_values, key=lambda x: x[1])
            worst_pair, min_val = pair_values_sorted[0]
            best_pair, max_val = pair_values_sorted[-1]
            avg_val = sum(v for _, v in pair_values) / len(pair_values)
            aggregate[field] = {
                "average": avg_val,
                "best": {"pair": best_pair, "value": max_val},
                "worst": {"pair": worst_pair, "value": min_val}
            }
 
        response_data = {
            "strategy": strategy,
            "position_type": position_type,
            "concurrency": concurrency,
            "pairs_analyzed": len(pairs_list),
            "aggregate": aggregate,
            "results": results
        }

        logger.info(f"Scan request - pairs: {pairs_list} | strategy: {strategy} | position_type: {position_type}")
        return jsonify(response_data)