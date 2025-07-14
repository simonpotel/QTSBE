from flask import jsonify, request
from datetime import datetime
from loguru import logger
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from stats.advanced import get_advanced_stats
from core.file_utils import get_file_data

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

        if not pair or not strategy:
            return jsonify({"error": "pair and strategy parameters are required"}), 400

        if position_type not in ['long', 'short']:
            return jsonify({"error": "position_type must be either 'long' or 'short'"}), 400

        if start_ts:
            start_ts = datetime.strptime(start_ts.strip("'").strip('"'), ts_format)
        if end_ts:
            end_ts = datetime.strptime(end_ts.strip("'").strip('"'), ts_format)

        multi_positions = bool(multi_positions) and (lambda s: s.lower() in {'true'})(multi_positions)

        data = get_file_data(pair)
        if not data:
            return jsonify({"error": f"No data found for pair {pair}"}), 404

        data = [(
            (str(row[0]) + " 00:00:00" if isinstance(row[0], str) and len(row[0]) == 10 
            else str(row[0]) if isinstance(row[0], (int, float)) 
            else row[0]),
            float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])
        ) for row in data]

        result = analyse_func(data, start_ts, end_ts, multi_positions, strategies[strategy], position_type)

        response_data = {
            "pair": pair,
            "strategy": strategy,
            "position_type": position_type,
            "data": data if details == "True" else [],
            "result": (
                result.indicators if details == "True" else [],
                result.positions,
                result.current_positions
            ),
            "stats": {
                "drawdown": get_drawdowns_stats(result),
                "positions": get_position_stats(result),
                "advanced": get_advanced_stats(result)
            }
        }

        logger.info(f"Analyse request - pair: {pair} | strategy: {strategy} | position_type: {position_type}")
        return jsonify(response_data) 