import os
import sys 
import importlib.util

# Add parent directories to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from loguru import logger
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from algo.data.file import *
from stats.drawdown import get_drawdowns_stats
from stats.positions import get_position_stats

debug_mode = True
strategies_folder = r"api/strategies"  # path to the folder containing strategy files
strategies = {}  # dictionary to store strategy functions

def reload_loguru_config():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")
    if debug_mode:
        logger.add(r"logs/debug.log", level="DEBUG")
    else:
        logger.add(r"logs/logs.log", level="INFO")

reload_loguru_config()

def import_strategies():
    for root, dirs, files in os.walk(strategies_folder):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                name_without_extension = os.path.splitext(file_name)[0]
                strategy_name = os.path.relpath(file_path, strategies_folder).replace(os.sep, '_').rsplit('.', 1)[0]
                spec = importlib.util.spec_from_file_location(name_without_extension, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                strategies[strategy_name] = module
                logger.debug(f"Content of {file_path} has been imported as module {strategy_name}")

app = Flask(__name__)
CORS(app, resources={r"/QTSBE/*": {"origins": "http://127.0.0.1"}})

@app.route('/QTSBE/<pair>/<strategy>')
def get_data(pair, strategy):
    start_ts = request.args.get('start_ts')
    end_ts = request.args.get('end_ts')

    data = get_file_data(pair)  
    prices = [float(entry[1].replace(',', '')) for entry in data]

    result = strategies[strategy].analyse(data, prices, start_ts, end_ts)

    response = jsonify({
        "pair": pair,
        "strategy": strategy,
        "data": data,
        "result": (
            result.indicators,
            result.positions,
            result.current_positions
        ),
        "stats": {
            "drawdown": get_drawdowns_stats(result),
            "positions": get_position_stats(result)
        }
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    logger.info(f"Request pair: {pair} | strategy: {strategy} | start_ts: {start_ts} | end_ts: {end_ts}")
    logger.debug(f"Request response: {response}")
    return response

if __name__ == '__main__':
    reload_loguru_config()
    import_strategies()
    logger.debug("List of all strategies: {}", list(strategies.keys()))
    logger.warning("API has been restarted.")
    app.run(debug=debug_mode)
