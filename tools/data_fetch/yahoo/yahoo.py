import os
import sys
import pandas as pd
from datetime import datetime
import yfinance as yf

sys.path.append(os.getcwd())

class YahooAPI:
    def __init__(self, data_dir='data/bank'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def download_and_save(self, tickers, interval='1d'):
        for ticker in tickers:
            data = yf.download(ticker, interval=interval)
            filepath = os.path.join(self.data_dir, f'{ticker}.csv')
            data.to_csv(filepath)

    def update_ohlcv(self, tickers, interval='1d'):
        for ticker in tickers:
            filepath = os.path.join(self.data_dir, f'{ticker}.csv')
            if os.path.exists(filepath):
                existing_data = pd.read_csv(filepath)
                last_date = existing_data['Date'].iloc[-1]
                last_datetime = datetime.strptime(last_date, '%Y-%m-%d')
                new_data = yf.download(ticker, start=last_datetime, interval=interval)
                new_data = new_data[new_data.index > last_datetime]

                if not new_data.empty:
                    new_data.to_csv(filepath, mode='a', header=False)
                    print(f"{ticker}: Data updated successfully")
                else:
                    print(f"{ticker}: No new data available")
            else:
                self.download_and_save([ticker], interval=interval)
                print(f"{ticker}: Data downloaded successfully")

if __name__ == "__main__":
    tickers = [
        'AAPL', 'MSFT' # ...
    ]
    
    yahoo_api = YahooAPI()
    yahoo_api.download_and_save(tickers, interval='1d')