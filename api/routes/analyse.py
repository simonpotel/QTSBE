from flask import jsonify, request
from datetime import datetime
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from stats.advanced import get_advanced_stats
from core.data_utils import get_data, clean_nans

def register_analyse_routes(app, strategies, analyse_func):
    @app.route('/QTSBE/analyse')
    def analyse_endpoint():
        ts_format = "%Y-%m-%d %H:%M:%S"
        pair = request.args.get('pair')
        strategy = request.args.get('strategy')
        start_ts = request.args.get('start_ts')
        end_ts = request.args.get('end_ts')
        multi_positions = request.args.get('multi_positions')
        details = request.args.get('details')
        position_type = request.args.get('position_type', 'long')

        if not pair or not strategy: return jsonify({"error": "pair and strategy required"}), 400
        if position_type not in ['long', 'short']: return jsonify({"error": "invalid position_type"}), 400

        if start_ts: start_ts = datetime.strptime(start_ts.strip("'").strip('"'), ts_format)
        if end_ts: end_ts = datetime.strptime(end_ts.strip("'").strip('"'), ts_format)
        multi_positions = multi_positions.lower() == 'true' if multi_positions else False

        data = get_data(pair)
        if not data: return jsonify({"error": "no data"}), 404

        data = [(str(r[0]) + " 00:00:00" if len(str(r[0])) == 10 else str(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])) for r in data]
        result = analyse_func(data, start_ts, end_ts, multi_positions, strategies[strategy], position_type)

        # Filter data (and indicators) by start_ts/end_ts so the response matches the requested range
        out_data = data
        out_indicators = result.indicators if details == "True" else {}
        if details == "True" and (start_ts or end_ts):
            filtered_indices = []
            for i, row in enumerate(data):
                row_ts = datetime.strptime(row[0], ts_format)
                if start_ts and row_ts < start_ts:
                    continue
                if end_ts and row_ts > end_ts:
                    break
                filtered_indices.append(i)
            out_data = [data[i] for i in filtered_indices]
            if result.indicators:
                out_indicators = {
                    k: [v[i] for i in filtered_indices]
                    for k, v in result.indicators.items()
                }
            else:
                out_indicators = {}

        res = {
            "pair": pair, "strategy": strategy, "position_type": position_type,
            "data": out_data if details == "True" else [],
            "result": (out_indicators if details == "True" else [], result.positions, result.current_positions),
            "stats": {"drawdown": get_drawdowns_stats(result), "positions": get_position_stats(result), "advanced": get_advanced_stats(result)}
        }
        return jsonify(clean_nans(res))