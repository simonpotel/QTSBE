import json
import os
import sys
import time
import threading
from flask import Flask, jsonify
from dotenv import load_dotenv
from loguru import logger
import traceback

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from tools.data.binance import BinanceAPI
from tools.data.yahoo import YahooAPI

load_dotenv()

# Setup logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.info('QTSBE Data Cron Started')

app = Flask(__name__)

# Global instances for health check
binance_api_global = None

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
            'message': 'Data cron service is running',
            'binance_connection': True
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Binance connection failed: {str(e)}',
            'binance_connection': False
        }), 500

def run_fetch_cycle():
    global binance_api_global
    
    config_path = 'config/data_cron.json'
    if not os.path.exists(config_path):
        logger.error(f"Config file not found: {config_path}")
        return

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return

    yahoo_api = YahooAPI()
    binance_api = BinanceAPI()
    
    if binance_api_global is None:
        binance_api_global = binance_api

    logger.info("Starting fetch cycle")

    # Yahoo data fetch
    if 'Yahoo' in config:
        for ticker, interval in config['Yahoo']:
            try:
                yahoo_api.update_ohlcv(ticker, interval)
            except Exception as e:
                logger.error(f"Error fetching Yahoo data for {ticker}: {e}")

    # Binance data fetch
    if 'Binance' in config:
        for symbol, interval in config['Binance']:
            try:
                binance_api.update_ohlcv(symbol, interval)
            except Exception as e:
                logger.error(f"Error fetching Binance data for {symbol}: {e}")

    logger.info("Fetch cycle completed")

def start_flask_server():
    """Start Flask server in a separate thread"""
    port = int(os.getenv('QTSBE_CRON_PORT', 5004))
    host = os.getenv('QTSBE_HOST', '0.0.0.0')
    debug = os.getenv('QTSBE_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting health check server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)

if __name__ == "__main__":
    # Start health check server
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Main loop
    while True:
        try:
            run_fetch_cycle()
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            logger.error(traceback.format_exc())
        
        # Wait 15 minutes between cycles by default or use env var
        interval = int(os.getenv('QTSBE_CRON_INTERVAL_SECONDS', 900))
        time.sleep(interval)
