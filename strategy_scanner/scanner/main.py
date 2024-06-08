import sys
import os
from colorama import init, Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm
import json

from scanner.utils import format_time
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data'))
from binance_api import BinanceAPI

init(autoreset=True)

class TokenScanner:
    def __init__(self):
        self.binance = BinanceAPI()

    def load_symbols(self):
        return self.binance.exchange.load_markets()

    def analyze_symbol(self, symbol, timeframe, strategy):
        url = f"http://127.0.0.1:5000/QTSBE/Binance_{symbol.replace('/', '')}_{timeframe}/{strategy}"
        response = requests.get(url)
        return response.json()

    def process_symbol(self, symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func):
        elapsed_time = time.time() - start_time
        avg_time_per_token = elapsed_time / index
        remaining_time = avg_time_per_token * (total_symbols - index)
        formatted_remaining_time = format_time(remaining_time)

        data = analysis_func(symbol, timeframe, strategy)
        return data, symbol, formatted_remaining_time

    def process_symbols(self, symbols, timeframe, strategy, fetch_latest_data, analysis_func):
        total_symbols = len(symbols)
        start_time = time.time()
        all_stats = []

        def process_symbol_wrapper(symbol, index):
            return self.process_symbol(symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func)

        if fetch_latest_data:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(self.binance.fetch_and_save_ohlcv, symbol, timeframe): symbol for symbol in symbols}
                print(f"{Fore.LIGHTMAGENTA_EX}Fetching and saving OHLCV data for all tokens...\r")
                for future in futures:
                    future.result()  

        with tqdm(total=total_symbols, desc="Processing scan", unit="symbol", ncols=100, dynamic_ncols=True, colour="BLUE") as pbar:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(process_symbol_wrapper, symbol, index): symbol for index, symbol in enumerate(symbols, start=1)}
                for index, future in enumerate(futures, start=1):
                    data, symbol, formatted_remaining_time = future.result()
                    if data and "stats" in data:
                        if data["stats"]["positions"]["average_position_duration"] != 0:
                            all_stats.append((symbol, data["stats"]))

                    pbar.set_postfix({
                        'Symbol': symbol,
                        'Time left': formatted_remaining_time,
                    })
                    pbar.update(1)

        pbar.write(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}All tokens processed!")
        all_stats_sorted = sorted(all_stats, key=lambda x: x[1]["positions"]["max_cumulative_ratio"], reverse=True)
        self.save_stats_to_json(all_stats_sorted)

    def save_stats_to_json(self, all_stats):
        result = {"tokens": []}
        for symbol, stats in all_stats:
            result["tokens"].append({
                "symbol": symbol,
                "stats": stats
            })
        with open('scan_result.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Results saved to scan_result.json")

    def scan(self, timeframe, strategy, fetch_latest_data):
        print(f"{Fore.WHITE}{Style.BRIGHT}Strategy Scanner: {Fore.LIGHTBLUE_EX}{strategy}\n{Fore.WHITE}Timeframe: {Fore.LIGHTBLUE_EX}{timeframe}\n{Fore.WHITE}Fetch Latest Data: {Fore.LIGHTBLUE_EX}{fetch_latest_data}")
        symbols = self.load_symbols()
        self.process_symbols(symbols, timeframe, strategy, fetch_latest_data, self.analyze_symbol)

