import os
import sys 
import importlib.util

# Add parent directories to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from loguru import logger
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from DEXcryptoLib.Lib import *
from algo.data.file import *
from stats.drawdown import get_drawdowns_stats

debug_mode = True
strategies_folder = r"api/strategies" # path to the folder containing strategy files
strategies = {} # dictionary to store strategy functions

def reload_loguru_config():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")  
    if debug_mode:
        logger.add(r"logs/debug.log", level="DEBUG")
    else:
        logger.add(r"logs/logs.log", level="INFO")
reload_loguru_config()

def import_strategies():
    for root, dirs, files in os.walk(strategies_folder): # loop through all files in the strategies folder and subfolders
        for file_name in files:
            if file_name.endswith(".py"): # check if the file is a Python file
                file_path = os.path.join(root, file_name)
                name_without_extension = os.path.splitext(file_name)[0]
                # create the strategy name with underscores for subdirectories
                strategy_name = os.path.relpath(file_path, strategies_folder).replace(os.sep, '_').rsplit('.', 1)[0]
                spec = importlib.util.spec_from_file_location(name_without_extension, file_path) # create a module specification
                module = importlib.util.module_from_spec(spec) # create a module from the specification
                spec.loader.exec_module(module) # load the module
                strategies[strategy_name] = module # store the module in the dictionary
                logger.debug(f"Content of {file_path} has been imported as module {strategy_name}")


app = Flask(__name__)
CORS(app, resources={r"/QTSBE/*": {"origins": "http://127.0.0.1"}})

@app.route('/QTSBE/<pair>/<strategy>')
def get_data(pair, strategy):
    data = get_file_data(pair) # get data (list of lists) with datetime and price (in str)
    prices = [float(entry[1].replace(',', ''))  for entry in data] # list of all prices in float 
    result = strategies[strategy].analyse(data, prices) # call the strategy func

    response = jsonify(
        {"pair": pair, # string
         "strategy": strategy, # string
         "data": data, # tab of tabs of 2 elements
         "result": (
             result.indicators,
             result.positions,
             result.current_position
             ), # result is an object of the class Positions in stats/positions.py
          "stats": 
             {"drawdown:": get_drawdowns_stats(result)}
        })
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    logger.info(f"Request pair: {pair} | strategy: {strategy}")
    logger.debug(f"Request response: {response}")

    # structure of a response:
    # the indicators set is unique to every strategies
    # (example for spot):
    #
    #{
    #    "data": [],
    #    "pair": "Binance_THEPAIR",
    #    "result": [
    #        {
    #            "mm_100": [],
    #            "mm_20": [],
    #            "rsi": []
    #        },
    #        [],
    #        {}
    #    ],
    #    "strategy": "spot"
    #}

    # see more details about the structure of "result" in strategies/default.py
    return response

if __name__ == '__main__':
    reload_loguru_config()
    import_strategies()
    logger.debug("List of all strategies: {}", list(strategies.keys()))
    logger.warning("API has been restarted.")
    app.run(debug=debug_mode)
