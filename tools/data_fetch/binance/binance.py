import ccxt
import pandas as pd
import os
from datetime import datetime, timedelta
import argparse
from colorama import Fore, Style, init
import concurrent.futures

init(autoreset=True)  # Initialize colorama

def fetch_ohlcv_batch(exchange, symbol, timeframe, since_timestamp):
    """
    Function to fetch a batch of OHLCV data.
    """
    print(f"{Fore.GREEN}Request{Fore.WHITE}: {Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}{timeframe}: {datetime.utcfromtimestamp(since_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S %H:%M:%S')}")
    return exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=1000)

class BinanceAPI:
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_and_save_ohlcv(self, symbol, timeframe):
        """
        Function to fetch OHLCV data and save it to a CSV file.
        """
        all_ohlcv = []  # List that will contain all data
        desired_timestamp = self.exchange.parse8601('2000-01-01T00:00:00Z')  # from now to desired_timestamp
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_timestamp = {
                executor.submit(fetch_ohlcv_batch, self.exchange, symbol, timeframe, desired_timestamp): desired_timestamp
            }
            
            while future_to_timestamp:
                for future in concurrent.futures.as_completed(future_to_timestamp):
                    timestamp = future_to_timestamp.pop(future)
                    ohlcv_batch = future.result()
                    
                    if len(ohlcv_batch) == 0:
                        break  # no data until the desired timestamp, stop code
                    
                    all_ohlcv += ohlcv_batch  # add the collected data to the others ones
                    desired_timestamp = ohlcv_batch[-1][0] + 1  # update the timestamp for the next request
                    
                    future_to_timestamp[executor.submit(fetch_ohlcv_batch, self.exchange, symbol, timeframe, desired_timestamp)] = desired_timestamp

        # convert data to DataFrame
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        # create the folder data/bank to store the data if it doesn't exist already
        os.makedirs('data/bank', exist_ok=True)
        # name of the CSV file
        filename = f"Binance_{symbol.replace('/', '')}_{timeframe}.csv"
        filepath = os.path.join('data/bank/', filename)
        # save content
        df.to_csv(filepath, index=False)
        print(f"{Fore.GREEN}All data has been saved in: {filepath}")
        return symbol
    
    def get_top_50_tokens_by_volume(self):
        """
        Function to print the top 50 tokens by trading volume.
        """
        markets = self.exchange.load_markets()  
        tickers = self.exchange.fetch_tickers()
        # create a list of tuples containing (symbol, volume) for each market
        volumes = [(symbol, tickers[symbol]['quoteVolume']) for symbol in tickers]
        # sort the list by volume in descending order and get the top 50 tokens
        top_50_volumes = sorted(volumes, key=lambda x: x[1], reverse=True)[:50]

        # print the top 50 tokens with their trading volumes
        for symbol, volume in top_50_volumes:
            print(f"{Fore.YELLOW}{symbol}: {volume}")

        return [symbol for symbol, volume in top_50_volumes]
    
    def fetch_tokens_daily_ohlcv(self, tokens_list):
        """
        Function to fetch and save daily OHLCV data for the top 50 tokens by trading volume.
        """
        for symbol in tokens_list:
            print(f"{Fore.CYAN}Fetching data for {symbol}")
            self.fetch_and_save_ohlcv(symbol, '1d')

    def get_recent_try_pairs(self):
        """
        Function to get the 100 most recent trading pairs that trade with TRY.
        """
        markets = self.exchange.load_markets()  # Load all markets
        try_pairs = [symbol for symbol in markets if 'TRY' in symbol.split('/')]

        # Since we don't have the exact creation date, we'll assume the order in the list is by recency
        recent_try_pairs = try_pairs[-100:]  # Get the last 100 pairs

        print(f"{Fore.LIGHTMAGENTA_EX}Recent 100 TRY trading pairs:")
        for pair in recent_try_pairs:
            print(pair)

        return recent_try_pairs

    def get_least_volatile_tokens(self, days):
        """
        Function to get the 50 tokens with the least price variation over the past X days.
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        start_timestamp = int(start_time.timestamp() * 1000)
        
        tickers = self.exchange.fetch_tickers()
        
        variations = []
        
        for symbol in tickers:
            print(f"{Fore.RED}Collected symbols: {len(variations)}/50 ({symbol})")
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', since=start_timestamp)
            if ohlcv:
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                if not df.empty:
                    price_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]
                    variations.append((symbol, price_change))
            
            if len(variations) >= 50:
                break
        
        least_volatile_tokens = sorted(variations, key=lambda x: abs(x[1]))[:50]
        for symbol, variation in least_volatile_tokens:
            print(f"{Fore.GREEN}{symbol}: {variation}")

        return [symbol for symbol, variation in least_volatile_tokens]

    def get_most_volatile_tokens(self, days):
        """
        Function to get the 50 tokens with the highest price variation over the past X days.
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        start_timestamp = int(start_time.timestamp() * 1000)
        
        tickers = self.exchange.fetch_tickers()
        
        variations = []
        
        for symbol in tickers:
            print(f"{Fore.BLUE}Collected symbols: {len(variations)}/50 ({symbol})")
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', since=start_timestamp)
            if ohlcv:
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                
                if not df.empty:
                    price_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]
                    variations.append((symbol, price_change))
            
            if len(variations) >= 50:
                break
                
        most_volatile_tokens = sorted(variations, key=lambda x: abs(x[1]), reverse=True)[:50]
        
        for symbol, variation in most_volatile_tokens:
            print(f"{Fore.MAGENTA}{symbol}: {variation}")

        return [symbol for symbol, variation in most_volatile_tokens]

    def update_ohlcv(self, symbol, timeframe='1d'):
        """
        Method to update the OHLCV data for a given symbol and timeframe.
        """
        filename = f"Binance_{symbol.replace('/', '')}_{timeframe}.csv"
        filepath = os.path.join('data/bank/', filename)
        
        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_existing['timestamp'] = pd.to_datetime(df_existing['timestamp'])
            last_timestamp = df_existing['timestamp'].max()
            since_timestamp = int(last_timestamp.timestamp() * 1000)
        else:
            df_existing = pd.DataFrame()
            since_timestamp = self.exchange.parse8601('2000-01-01T00:00:00Z')

        new_data = self.exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp)
        if not new_data:
            print(f"{Fore.RED}No new data for {symbol}")
            return

        df_new = pd.DataFrame(new_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_new['timestamp'] = pd.to_datetime(df_new['timestamp'], unit='ms')
        
        if not df_existing.empty:
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['timestamp'], keep='last').reset_index(drop=True)
        else:
            df_combined = df_new
        
        df_combined.to_csv(filepath, index=False)
        print(f"{Fore.GREEN}Updated data has been saved in: {filepath}")

    def update_ohlcv_for_symbols(self, symbols, timeframe='1d'):
        """Method to update the OHLCV data for a list of symbols."""
        for symbol in symbols:
            print(f"{Fore.CYAN}Updating data for {symbol}")
            self.update_ohlcv(symbol, timeframe)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and save OHLCV data from Binance.')
    parser.add_argument('-symbol', type=str, default='BTC/USDC', help='The trading pair symbol, e.g., “BTC/USDC”.')
    parser.add_argument('-timeframe', type=str, default='1d', help='The timeframe for the OHLCV data, e.g., “1d”.')