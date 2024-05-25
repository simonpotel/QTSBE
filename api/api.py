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

debug_mode = True
strategies_folder = r"api/strategies" # path to the folder containing strategy files
strategies = {} # dictionary to store strategy functions

def reload_loguru_config():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")  
    if debug_mode:
        logger.add(r"logs\debug.log", level="DEBUG")
    else:
        logger.add(r"logs\logs.log", level="INFO")
reload_loguru_config()

def import_strategies():
    for file_name in os.listdir(strategies_folder): # loop through all files in the strategies folder
        file_path = os.path.join(strategies_folder, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".py"): # check if the file is a Python file
            name_without_extension = os.path.splitext(file_name)[0] # get the file name without the .py extension
            spec = importlib.util.spec_from_file_location(name_without_extension, file_path) # create a module specification
            module = importlib.util.module_from_spec(spec) # create a module from the specification
            spec.loader.exec_module(module) # load the module
            strategies[name_without_extension] = module # store the module in the dictionary
            logger.debug(f"Content of strategies/{file_name} has been imported as module {name_without_extension}")

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
         "result": result # indicators, trades, position
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
