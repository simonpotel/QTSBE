import os
import sys 

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
print(os.getcwd())

# Add parent directories to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from DEXcryptoLib.Lib import *
from algo.algo import *


app = Flask(__name__)
CORS(app, resources={r"/QTSBE/*": {"origins": "http://127.0.0.1"}})

@app.route('/QTSBE/<pair>/<algo>')
def get_data(pair, algo):
    response = jsonify(
        {"pair": pair, 
         "algo": algo}
        )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(debug=True)
