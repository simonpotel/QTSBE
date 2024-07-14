import os
import pandas as pd
from binance_api import BinanceAPI
from colorama import Fore
from loguru import logger

def get_most_recent_ohlcv(csv_filepath):
    df = pd.read_csv(csv_filepath)
    most_recent_ohlcv = df.iloc[-1].to_dict()
    return most_recent_ohlcv

def main():
    binance_data = BinanceAPI()
    csv_dir = 'data/bank'

    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_filepath = os.path.join(csv_dir, csv_file)
        symbol_timeframe = os.path.splitext(csv_file)[0].replace('Binance_', '')
        symbol, timeframe = symbol_timeframe.split('_')
        
        most_recent_ohlcv_csv = get_most_recent_ohlcv(csv_filepath)

        try:
            ohlcv_data = binance_data.exchange.fetch_ohlcv(symbol, timeframe)

            if ohlcv_data:
                most_recent_ohlcv_binance = ohlcv_data[-1]

                if most_recent_ohlcv_csv != most_recent_ohlcv_binance:
                    logger.info(f"{Fore.GREEN}Updating CSV file: {csv_file}")
                    all_ohlcv = binance_data.fetch_and_save_ohlcv(symbol, timeframe)
                    
                    if all_ohlcv:
                        logger.info(f"{Fore.GREEN}CSV file updated successfully: {csv_file}")
                else:
                    logger.info(f"{Fore.YELLOW}No update needed for CSV file: {csv_file}")
            else:
                logger.warning(f"{Fore.RED}Failed to fetch OHLCV data for symbol: {symbol}, timeframe: {timeframe}")
        except Exception as e:
            logger.error(f"{Fore.RED}Error fetching OHLCV data from Binance for {symbol}_{timeframe}: {e}")

if __name__ == "__main__":
    main()