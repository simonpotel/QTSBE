import ccxt
import pandas as pd
import os
from datetime import datetime
import argparse

class BinanceAPI:
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_and_save_ohlcv(self, symbol, timeframe):
        """
        Function to fetch OHLCV data and save it to a CSV file.
        """
        all_ohlcv = []  # List that will contain all data
        desired_timestamp = self.exchange.parse8601('2000-01-01T00:00:00Z')  # from now to desired_timestamp
        while True: 
            print(f"Request: {timeframe} {datetime.utcfromtimestamp(desired_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
            ohlcv_batch = self.exchange.fetch_ohlcv(symbol, timeframe, since=desired_timestamp, limit=1000)
            if len(ohlcv_batch) == 0:
                break  # no data until the desired timestamp, stop code
            all_ohlcv += ohlcv_batch  # add the collected data to the others ones
            desired_timestamp = ohlcv_batch[-1][0] + 1  # update the timestamp for the next request

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
        print(f"All data has been saved in: {filepath}")

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
            print(f"{symbol}: {volume}")

        return [symbol for symbol, volume in top_50_volumes]
    
    def fetch_top_50_tokens_daily_ohlcv(self):
        """
        Function to fetch and save daily OHLCV data for the top 50 tokens by trading volume.
        """
        top_50_tokens = self.get_top_50_tokens_by_volume()
        for symbol in top_50_tokens:
            print(f"Fetching data for {symbol}")
            self.fetch_and_save_ohlcv(symbol, '1d')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and save OHLCV data from Binance.')
    parser.add_argument('-symbol', type=str, default='BTC/USDT', help='The trading pair symbol, e.g., "BTC/USDT".')
    parser.add_argument('-timeframe', type=str, default='1d', help='The timeframe for the OHLCV data, e.g., "1d".')

    args = parser.parse_args()

    binance_data = BinanceAPI()
    binance_data.fetch_and_save_ohlcv(args.symbol, args.timeframe)
    
