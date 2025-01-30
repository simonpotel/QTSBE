from flask import jsonify, request
from datetime import datetime
from loguru import logger
from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from core.file_utils import get_file_data

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
            for row in data:
                if len(row[0]) == 10:
                    row[0] += " 00:00:00"

            result = analyse_func(data, start_ts, end_ts, multi_positions, custom_strategy)

            response_data = {
                "pair": pair,
                "strategy": "custom",
                "data": data if details == "True" else [],
                "result": (
                    result.indicators if details == "True" else [],
                    result.positions,
                    result.current_positions
                ),
                "stats": {
                    "drawdown": get_drawdowns_stats(result),
                    "positions": get_position_stats(result)
                }
            }

            logger.info(f"Custom analyse request - pair: {pair} | start_ts: {start_ts} | end_ts: {end_ts} | multi_positions: {multi_positions} | details: {details}")
            return jsonify(response_data)

        except Exception as e:
            error_msg = f"Error in custom strategy execution: {str(e)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 400 