import json
import os
import sys
import time
from loguru import logger

sys.path.append(os.getcwd())

from tools.data_fetch.binance.binance import BinanceAPI
from tools.data_fetch.yahoo.yahoo import YahooAPI

log_directory = "tools/auto_fetch/logs"
os.makedirs(log_directory, exist_ok=True)
log_path = os.path.join(log_directory, "{time:YYYY-MM-DD}.log")

logger.add(log_path, rotation="00:00", retention="7 days", level="INFO")
logger.info('Start')

# Amount of logs for each day :
# If we fetch every min, and we have 2 logs (normally) :
# 2 * 60 * 24 = 2880 logs on a file every day.

# SUCCESS :  logs for start and end of cycles.
# INFO : logs for Start of the script
# ERROR : logs for errors using Binance/Yahoo api.

def main():
    with open('tools/auto_fetch/config.json', 'r') as f:
        config = json.load(f)

    yahoo_api = YahooAPI()
    binance_api = BinanceAPI()

    while True:
        logger.success(f"Starting fetch cycle")

        try:
            for ticker, interval in config['Yahoo']:
                yahoo_api.update_ohlcv(ticker, interval)
        except Exception as e:
            logger.error(f"Error fetching Yahoo data: {e}")

        try:
            for symbol, interval in config['Binance']:
                binance_api.update_ohlcv(symbol, interval)
        except Exception as e:
            logger.error(f"Error fetching Binance data: {e}")

        logger.success(f"Fetch cycle completed")

        time.sleep(60)

if __name__ == "__main__":
    main()