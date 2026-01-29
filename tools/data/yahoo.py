import os
import pandas as pd
from datetime import datetime
import yfinance as yf
from colorama import Fore

class YahooAPI:
    def __init__(self, data_dir='data/bank'):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def download_and_save(self, tickers, interval='1d'):
        for ticker in tickers:
            try:
                print(f"{Fore.CYAN}Downloading data for {ticker}")
                data = yf.download(ticker, interval=interval)
                if data.empty:
                    print(f"{Fore.RED}No data found for {ticker}")
                    continue
                
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                
                data.reset_index(inplace=True)
                data = data.rename(columns={
                    'Date': 'timestamp', 
                    'Open': 'open', 
                    'High': 'high', 
                    'Low': 'low', 
                    'Close': 'close', 
                    'Volume': 'volume'
                })
                
                cols_to_keep = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                data = data[[c for c in cols_to_keep if c in data.columns]]
                
                clean_ticker = ticker.replace('/', '_')
                filepath = os.path.join(self.data_dir, f'Yahoo_{clean_ticker}_{interval}.csv')
                data.to_csv(filepath, index=False)
                print(f"{Fore.GREEN}Data saved in: {filepath}")
            except Exception as e:
                print(f"{Fore.RED}Error downloading {ticker}: {e}")

    def update_ohlcv(self, ticker, interval='1d'):
        clean_ticker = ticker.replace('/', '_')
        filepath = os.path.join(self.data_dir, f'Yahoo_{clean_ticker}_{interval}.csv')
        if os.path.exists(filepath):
            try:
                existing_data = pd.read_csv(filepath)
                if existing_data.empty:
                    self.download_and_save([ticker], interval=interval)
                    return
                    
                last_date = existing_data['timestamp'].iloc[-1]
                try:
                    last_datetime = datetime.strptime(str(last_date), '%Y-%m-%d')
                except ValueError:
                    last_datetime = pd.to_datetime(last_date)

                new_data = yf.download(ticker, start=last_datetime, interval=interval)
                if not new_data.empty:
                    if isinstance(new_data.columns, pd.MultiIndex):
                        new_data.columns = new_data.columns.get_level_values(0)

                    new_data.reset_index(inplace=True)
                    new_data = new_data.rename(columns={
                        'Date': 'timestamp', 
                        'Open': 'open', 
                        'High': 'high', 
                        'Low': 'low', 
                        'Close': 'close', 
                        'Volume': 'volume'
                    })
                    
                    if 'timestamp' in new_data.columns:
                        new_data['timestamp'] = pd.to_datetime(new_data['timestamp']).dt.strftime('%Y-%m-%d')
                        new_data = new_data[new_data['timestamp'] > str(last_date)]

                    if not new_data.empty:
                        cols_to_keep = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                        new_data = new_data[[c for c in cols_to_keep if c in new_data.columns]]
                        new_data.to_csv(filepath, mode='a', header=False, index=False)
                        print(f"{Fore.GREEN}{ticker}: Data updated successfully")
                    else:
                        print(f"{Fore.YELLOW}{ticker}: No new data available")
                else:
                    print(f"{Fore.YELLOW}{ticker}: No new data available")
            except Exception as e:
                print(f"{Fore.RED}Error updating {ticker}: {e}")
        else:
            self.download_and_save([ticker], interval=interval)
