import sys
import os
from colorama import init, Fore
import time
from concurrent.futures import ThreadPoolExecutor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data'))
from binance_api import BinanceAPI
import requests
from scanner.utils import format_time, print_progress, print_analysis, print_best_pair

init(autoreset=True)

def scan_tokens(timeframe, strategy, fetch_latest_data):
    binance = BinanceAPI()
    symbols = binance.exchange.load_markets() 
    total_symbols = len(symbols)
    start_time = time.time()
    best_pair = ""
    max_cumulative_ratio = 0
    tab_best_pairs = []

    def process_symbol(symbol, index, total_symbols, start_time):
        progress_percent = (index / total_symbols) * 100
        elapsed_time = time.time() - start_time
        avg_time_per_token = elapsed_time / index
        remaining_time = avg_time_per_token * (total_symbols - index)
        formatted_remaining_time = format_time(remaining_time)
        print_progress(symbol, index, total_symbols, progress_percent, formatted_remaining_time)

        cumulative_ratio = analyze_symbol(symbol, timeframe, strategy)
        print_analysis(symbol, index, total_symbols, cumulative_ratio)
        return cumulative_ratio, symbol

    if fetch_latest_data:
        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = {executor.submit(binance.fetch_and_save_ohlcv, symbol, timeframe): symbol for symbol in symbols}
            print(f"{Fore.LIGHTMAGENTA_EX}Fetching and saving OHLCV data for all tokens...\z")
            for index, future in enumerate(futures, start=1):
                symbol = future.result()
                cumulative_ratio, symbol = process_symbol(symbol, index, total_symbols, start_time)
                if cumulative_ratio > max_cumulative_ratio:
                    max_cumulative_ratio = cumulative_ratio
                    best_pair = symbol
                    tab_best_pairs.append((best_pair, max_cumulative_ratio))
                print_best_pair(best_pair, max_cumulative_ratio)
    else:
        for index, symbol in enumerate(symbols, start=1):
            cumulative_ratio, symbol = process_symbol(symbol, index, total_symbols, start_time)
            if cumulative_ratio > max_cumulative_ratio:
                max_cumulative_ratio = cumulative_ratio
                best_pair = symbol
                tab_best_pairs.append((best_pair, max_cumulative_ratio))
            print_best_pair(best_pair, max_cumulative_ratio)
            print(tab_best_pairs)

    print(f"{Fore.GREEN}All tokens processed!\r")
    print(f"{Fore.WHITE}Best Pairs for this strategy: {Fore.GREEN}{tab_best_pairs}\r")

def analyze_symbol(symbol, timeframe, strategy):
    url = f"http://127.0.0.1:5000/QTSBE/Binance_{symbol.replace('/', '')}_{timeframe}/{strategy}"
    response = requests.get(url)
    data = response.json()
    cumulative_ratio = data["stats"]["positions"]["max_cumulative_ratio"]
    return cumulative_ratio
