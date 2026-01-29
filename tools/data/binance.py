import ccxt
import pandas as pd
import os
from colorama import Fore

class BinanceAPI:
    def __init__(self):
        self.exchange = ccxt.binance()

    def update_ohlcv(self, symbol, timeframe='1d'):
        """
        Method to update the OHLCV data for a given symbol and timeframe.
        """
        filename = f"Binance_{symbol.replace('/', '')}_{timeframe}.csv"
        filepath = os.path.join('data/bank/', filename)
        os.makedirs('data/bank/', exist_ok=True)
        
        if os.path.exists(filepath):
            try:
                df_existing = pd.read_csv(filepath)
                df_existing['timestamp'] = pd.to_datetime(df_existing['timestamp'])
                last_timestamp = df_existing['timestamp'].max()
                since_timestamp = int(last_timestamp.timestamp() * 1000)
            except Exception as e:
                print(f"{Fore.RED}Error reading existing file {filepath}: {e}")
                df_existing = pd.DataFrame()
                since_timestamp = self.exchange.parse8601('2000-01-01T00:00:00Z')
        else:
            df_existing = pd.DataFrame()
            since_timestamp = self.exchange.parse8601('2000-01-01T00:00:00Z')

        try:
            new_data = self.exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp)
            if not new_data:
                print(f"{Fore.YELLOW}No new data for {symbol}")
                return

            df_new = pd.DataFrame(new_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df_new['timestamp'] = pd.to_datetime(df_new['timestamp'], unit='ms')
            
            if not df_existing.empty:
                df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['timestamp'], keep='last').reset_index(drop=True)
            else:
                df_combined = df_new
            
            df_combined.to_csv(filepath, index=False)
            print(f"{Fore.GREEN}Updated data has been saved in: {filepath}")
        except Exception as e:
            print(f"{Fore.RED}Error updating {symbol}: {e}")
