import json
import os
import sys
import time
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv
from loguru import logger
import traceback

sys.path.append(os.getcwd())

from tools.data_fetch.binance.binance import BinanceAPI
from tools.data_fetch.yahoo.yahoo import YahooAPI

load_dotenv()

log_directory = "logs/auto_fetch"
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "{time:YYYY-MM-DD}.log")

logger.add(log_path, rotation="00:00", retention="7 days", level="INFO")
logger.info('Start')

app = Flask(__name__)

# Global Binance API instance for health check
binance_api_global = None

# Amount of logs for each day :
# If we fetch every min, and we have 2 logs (normally) :
# 2 * 60 * 24 = 2880 logs on a file every day.

# SUCCESS :  logs for start and end of cycles.
# INFO : logs for Start of the script
# ERROR : logs for errors using Binance/Yahoo api.

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint that verifies Binance connection"""
    try:
        if binance_api_global is None:
            return jsonify({
                'status': 'error',
                'message': 'Binance API not initialized',
                'binance_connection': False
            }), 500
        
        binance_api_global.exchange.fetch_time()
        
        return jsonify({
            'status': 'healthy',
            'message': 'Auto-fetch service is running',
            'binance_connection': True
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Binance connection failed: {str(e)}',
            'binance_connection': False
        }), 500

def main():
    global binance_api_global
    
    with open('config/auto_fetch.json', 'r') as f:
        config = json.load(f)

    yahoo_api = YahooAPI()
    binance_api = BinanceAPI()
    
    if binance_api_global is None:
        binance_api_global = binance_api

    logger.success(f"Starting fetch cycle")

    try:
        for ticker, interval in config['Yahoo']:
            yahoo_api.update_ohlcv(ticker, interval)
    except Exception as e:
        logger.error(f"Error fetching Yahoo data: {e}")
        logger.error(traceback.format_exc())

    try:
        for symbol, interval in config['Binance']:
            binance_api.update_ohlcv(symbol, interval)
    except Exception as e:
        logger.error(f"Error fetching Binance data: {e}")
        logger.error(traceback.format_exc())

    logger.success(f"Fetch cycle completed")

def start_flask_server():
    """Start Flask server in a separate thread"""
    port = int(os.getenv('FLASK_QTSBE_AUTO_FETCH_PORT', 5004))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    while True:
        main()
        time.sleep(15)
