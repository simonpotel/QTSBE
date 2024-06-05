import sys
import os
from colorama import init, Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))
from binance_api import BinanceAPI
import requests
import json

init(autoreset=True)

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} min {seconds} sec"

def scan_tokens(timeframe, strategy):
    binance = BinanceAPI()
    symbols = binance.exchange.load_markets() 
    total_symbols = len(symbols)
    start_time = time.time()
    best_pair = ""
    max_cumulative_ratio = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(binance.fetch_and_save_ohlcv, symbol, timeframe) for symbol in symbols]
        print(f"{Fore.LIGHTMAGENTA_EX}Fetching and saving OHLCV data for all tokens...\r")
        for index, future in enumerate(futures, start=1):
            symbol = future.result()
            progress_percent = (index / total_symbols) * 100
            elapsed_time = time.time() - start_time
            avg_time_per_token = elapsed_time / (index - 1) if index > 1 else 0
            remaining_time = avg_time_per_token * (total_symbols - index)
            formatted_remaining_time = format_time(remaining_time)
            print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}{progress_percent:.2f}{Fore.WHITE}% complete ({Fore.YELLOW}Time left: {Fore.GREEN}{formatted_remaining_time}{Fore.WHITE})\r")
            print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}Analyse...{Fore.WHITE}\r")
            url = f"http://127.0.0.1:5000/QTSBE/Binance_{symbol.replace('/', '')}_{timeframe}/{strategy}"
            response = requests.get(url)
            data = response.json()
            cumulative_ratio = data["stats"]["positions"]["max_cumulative_ratio"]
            print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}CR: {cumulative_ratio}{Fore.WHITE}\r")

            if cumulative_ratio > max_cumulative_ratio:
                max_cumulative_ratio = cumulative_ratio
                best_pair = symbol
            print(f"{Fore.RED}Best Pair: ({best_pair}) - CR: {max_cumulative_ratio}\r")



    print(f"{Fore.GREEN}All tokens processed!\r")

if __name__ == "__main__":
    scan_tokens('1d', 'QTS_pumpNC')
