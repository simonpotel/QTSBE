import os
import pandas as pd
from datetime import datetime
import yfinance as yf
from colorama import Fore, init

init(autoreset=True)  # Initialize colorama

class YahooAPI:
    def __init__(self, data_dir='data/bank'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def download_and_save(self, tickers, interval='1d'):
        for ticker in tickers:
            print(f"{Fore.CYAN}Downloading data for {ticker}")
            data = yf.download(ticker, interval=interval)
            data.reset_index(inplace=True)
            data = data.rename(columns={
                'Date': 'timestamp', 
                'Open': 'open', 
                'High': 'high', 
                'Low': 'low', 
                'Close': 'close', 
                'Volume': 'volume'
            }).drop(columns=['Adj Close'])
            ticker = ticker.replace('/', '_')
            filepath = os.path.join(self.data_dir, f'Yahoo_{ticker}_{interval}.csv')
            data.to_csv(filepath, index=False)
            print(f"{Fore.GREEN}Data saved in: {filepath}")

    def update_ohlcv(self, ticker, interval='1d'):
        filepath = os.path.join(self.data_dir, f'Yahoo_{ticker}_{interval}.csv')
        if os.path.exists(filepath):
            existing_data = pd.read_csv(filepath)
            last_date = existing_data['timestamp'].iloc[-1]
            last_datetime = datetime.strptime(last_date, '%Y-%m-%d')
            print(f"Last date in existing data: {last_date}")

            new_data = yf.download(ticker, start=last_datetime, interval=interval)
            new_data.reset_index(inplace=True)
            new_data = new_data.rename(columns={
                'Date': 'timestamp', 
                'Open': 'open', 
                'High': 'high', 
                'Low': 'low', 
                'Close': 'close', 
                'Volume': 'volume'
            }).drop(columns=['Adj Close'])
            new_data = new_data[new_data['timestamp'] > last_date]

            if not new_data.empty:
                new_data.to_csv(filepath, mode='a', header=False, index=False)
                print(f"{Fore.GREEN}{ticker}: Data updated successfully")
            else:
                print(f"{Fore.YELLOW}{ticker}: No new data available")
        else:
            self.download_and_save([ticker], interval=interval)
            print(f"{Fore.GREEN}{ticker}: Data downloaded successfully")

    def update_ohlcv_for_tickers(self, tickers, interval):
        for ticker in tickers:
            print(f"{Fore.CYAN}Updating data for {ticker}")
            self.update_ohlcv(ticker, interval)

if __name__ == "__main__":
    tickers = [
        'AAPL', 'MSFT'  # Add more tickers as needed
    ]
    
    yahoo_api = YahooAPI()
    yahoo_api.download_and_save(tickers, interval='1d')