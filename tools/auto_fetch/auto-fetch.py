import json 
import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.binance.binance import BinanceAPI
from tools.data_fetch.yahoo.yahoo import YahooAPI

def main():
    with open('tools/auto_fetch/config.json', 'r') as f:
        config = json.load(f)

    yahoo_api = YahooAPI()
    for ticker, interval in config['Yahoo']:
        yahoo_api.update_ohlcv(ticker, interval)

    binance_api = BinanceAPI()
    for symbol, interval in config['Binance']:
        binance_api.update_ohlcv(symbol, interval)

if __name__ == "__main__":
    main()