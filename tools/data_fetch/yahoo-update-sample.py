import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.yahoo.yahoo import YahooAPI

if __name__ == "__main__":
    tickers = [
        'TSLA', # TSLA: Tesla Inc. - Manufacturer of electric vehicles and renewable energy solutions.
        'AMZN' # AMZN: Amazon.com Inc. - E-commerce giant and provider of cloud services (AWS).
    ]

    yahoo_api = YahooAPI()
    yahoo_api.update_ohlcv(tickers, interval='1d')