import sys
import os
from colorama import init, Fore, Style
import time

init(autoreset=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data')
sys.path.append(data_dir)

from binance_api import BinanceAPI

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} min {seconds} sec"

def fetch_and_save_all_tokens_ohlcv(timeframe):
    binance = BinanceAPI()
    symbols = binance.exchange.load_markets()  
    total_symbols = len(symbols)
    start_time = time.time()  
    
    for index, symbol in enumerate(symbols, start=1):
        progress_percent = (index / total_symbols) * 100
        
        elapsed_time = time.time() - start_time
        avg_time_per_token = elapsed_time / (index - 1) if index > 1 else 0
        remaining_time = avg_time_per_token * (total_symbols - index)
        formatted_remaining_time = format_time(remaining_time)
        print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}{progress_percent:.2f}{Fore.WHITE}% complete ({Fore.YELLOW}Time left: {Fore.GREEN}{formatted_remaining_time}{Fore.WHITE})", end='\r')
        time.sleep(0.1)
        binance.fetch_and_save_ohlcv(symbol, timeframe)

    print(f"\n{Fore.GREEN}All tokens processed!")

if __name__ == "__main__":
    fetch_and_save_all_tokens_ohlcv('1d')
