from stats.positions import get_position_stats
from stats.drawdown import get_drawdowns_stats
from algo.data.file import *
from stats.trades import Positions
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response
from loguru import logger
import os
import sys
import importlib.util
from datetime import datetime

# Add parent directories to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))

debug_mode = True
# path to the folder containing strategy files
strategies_folder = r"api/strategies"
strategies = {}  # dictionary to store strategy functions


def reload_loguru_config():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")
    if debug_mode:
        logger.add(r"api/logs/debug.log", level="DEBUG")
    else:
        logger.add(r"api/logs/logs.log", level="INFO")


reload_loguru_config()


def import_signals_and_indicators(strategies_folder="strategies"):
    strategies = {}
    for root, dirs, files in os.walk(strategies_folder):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                name_without_extension = os.path.splitext(file_name)[0]
                strategy_name = os.path.relpath(file_path, strategies_folder).replace(os.sep, '_').rsplit('.', 1)[0]
                try:
                    spec = importlib.util.spec_from_file_location(name_without_extension, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    buy_signal_func = getattr(module, 'buy_signal', None)
                    sell_signal_func = getattr(module, 'sell_signal', None)
                    indicators_class = getattr(module, 'Indicators', None)
                    if buy_signal_func and sell_signal_func and indicators_class:
                        strategies[strategy_name] = {
                            "buy_signal": buy_signal_func,
                            "sell_signal": sell_signal_func,
                            "Indicators": indicators_class
                        }
                        logger.debug(f"Imported strategy '{strategy_name}' from {file_path}")
                except Exception as e:
                    logger.error(f"Failed to import module '{strategy_name}' from {file_path}: {e}")
    logger.info(f'Strategies: {strategies}')
    return strategies


app = Flask(__name__)
CORS(app, resources={r"/QTSBE/*": {"origins": "http://127.0.0.1"}})

def analyse(data, start_ts, end_ts, multi_positions, strategy):
    positions = Positions()
    indicators = strategy["Indicators"](data)

    positions.indicators = {key: list(value) for key, value in indicators.indicators.items()}

    for i in range(len(data)):
        data_date = datetime.strptime(data[i][0], "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
        if start_ts and data_date < start_ts:
            continue
        if end_ts and data_date > end_ts:
            break

        if not positions.current_positions or multi_positions:
            signal = strategy["buy_signal"](positions.current_positions, data, i, indicators.indicators)
            if signal == 1:
                positions.add_position(
                    buy_index=i,
                    buy_price=data[i][3],
                    buy_date=data_date.strftime("%Y-%m-%d %H:%M:%S"),
                    buy_signals={'Buy_Signal':signal}
                )

        for position in positions.current_positions[:]:
            signal = strategy["sell_signal"](position, data, i, indicators.indicators)
            if signal == -1:
                positions.close_position(
                    buy_index=position['buy_index'],
                    sell_index=i,
                    sell_price=data[i][2],
                    sell_date=data_date.strftime("%Y-%m-%d %H:%M:%S"),
                    sell_signals={'Sell_Signal': signal}
                )
            elif signal == 1 and multi_positions:
                positions.add_position(
                    buy_index=i,
                    buy_price=data[i][3],
                    buy_date=data_date.strftime("%Y-%m-%d %H:%M:%S"),
                    buy_signals={'Buy_Signal':signal}
                )

    return positions

@app.route('/QTSBE/<pair>/<strategy>')
def get_data(pair, strategy):
    ts_format = "%Y-%m-%d %H:%M:%S"
    start_ts = request.args.get('start_ts')
    end_ts = request.args.get('end_ts')
    multi_positions = request.args.get('multi_positions')
    details = request.args.get('details')
    multi_positions = bool(multi_positions) and (
        lambda s: s.lower() in {'true'})(multi_positions)
    if start_ts:
        start_ts = datetime.strptime(start_ts, ts_format)
    if end_ts:
        end_ts = datetime.strptime(end_ts, ts_format)

    data = get_file_data(pair)
    for row in data:
        if len(row[0]) == 10:  # Check if the date string is in the format "YYYY-MM-DD"
            row[0] += " 00:00:00"

    result = analyse(data, start_ts, end_ts, multi_positions, strategies[strategy])

    response_data = {
        "pair": pair,
        "strategy": strategy,
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

    response = jsonify(response_data)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    logger.info(f"Request pair: {pair} | strategy: {strategy} | start_ts: {
                start_ts} | end_ts: {end_ts} | multi_positions: {multi_positions} | details: {details}")
    logger.debug(f"Request response: {response}")
    return response


if __name__ == '__main__':
    reload_loguru_config()
    strategies = import_signals_and_indicators(strategies_folder)
    logger.debug("List of all strategies: {}", list(strategies.keys()))
    logger.warning("API has been restarted.")
    app.run(debug=debug_mode)
