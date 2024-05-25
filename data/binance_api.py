import ccxt
import pandas as pd
import os
from datetime import datetime
import argparse

def fetch_and_save_ohlcv(symbol, timeframe):
    """
    Function that will connect from now to the timeframe that we decide the data of a symbol.
    It will make multiple requests and add them to eachother, because the API limits the results to 1000
    """
    exchange = ccxt.binance() # Binance obj instance
    all_ohlcv = [] # List thats will contains all data
    desired_timestamp = exchange.parse8601('2000-01-01T00:00:00Z') # From now to desired_timestamp
    while True: 
        print(f"Request: {timeframe} {datetime.utcfromtimestamp(desired_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
        ohlcv_batch = exchange.fetch_ohlcv(symbol, timeframe, since=desired_timestamp, limit=1000)
        if len(ohlcv_batch) == 0: break # No data until the desired timestamp, stop code
        all_ohlcv += ohlcv_batch # add the collected data to the others ones
        desired_timestamp = ohlcv_batch[-1][0] + 1 # update the timestamp for the next request
        
    # convert data to timestamp
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # convert timestamp to data
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # create the folder data/bank to stock the data if it doesnt exists already
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/bank', exist_ok=True)
    # name of the csv file
    filename = f"Binance_{symbol.replace('/', '')}_{timeframe}.csv"
    filepath = os.path.join('data/bank/', filename)
    # save content
    df.to_csv(filepath, index=False)
    print(f"All Data has been saved in: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and save OHLCV data from Binance.')
    parser.add_argument('-symbol', type=str, default='BTC/USDT', help='The trading pair symbol, e.g., "BTC/USDT".')
    parser.add_argument('-timeframe', type=str, default='1d', help='The timeframe for the OHLCV data, e.g., "1d".')
    args = parser.parse_args()

    fetch_and_save_ohlcv(args.symbol, args.timeframe)
