import os
import sys 
# Add parent directories to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from loguru import logger
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from DEXcryptoLib.Lib import *

from algo.algo import *
from algo.data.file import *

debug_mode = True

app = Flask(__name__)
CORS(app, resources={r"/QTSBE/*": {"origins": "http://127.0.0.1"}})
@app.route('/QTSBE/<pair>/<algo>')
def get_data(pair, algo):
    response = jsonify(
        {"pair": pair, 
         "data": get_file_data(pair)}
        )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    logger.info(f"Request pair: {pair} | algo: {algo}")
    logger.debug(f"Request response: {response}")
    return response

if __name__ == '__main__':
    logger.remove()
    if debug_mode:
        logger.add("logs\debug.log", level="DEBUG")
        logger.add(sys.stdout, level="DEBUG")  
    else:
        logger.add("logs\logs.log", level="INFO")  
        logger.add(sys.stdout, level="INFO")  

    logger.warning("API has been restarted.")
    app.run(debug=debug_mode)

