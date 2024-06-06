import sys
import os
from colorama import init, Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from tqdm import tqdm

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

    def process_symbol(self, symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func, pbar):
        elapsed_time = time.time() - start_time
        avg_time_per_token = elapsed_time / index
        remaining_time = avg_time_per_token * (total_symbols - index)
        formatted_remaining_time = format_time(remaining_time)

        data = analysis_func(symbol, timeframe, strategy)
        return data, symbol, formatted_remaining_time

    def process_symbols(self, symbols, timeframe, strategy, fetch_latest_data, analysis_func, task_name):
        total_symbols = len(symbols)
        start_time = time.time()
        best_pair = ""
        latest_buy_date = datetime.min
        max_cumulative_ratio = 0
        tab_best_pairs = []

        def process_symbol_wrapper(symbol, index):
            return self.process_symbol(symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func, pbar)

        with tqdm(total=total_symbols, desc="Processing scan", unit="symbol", ncols=100, dynamic_ncols=True, colour="YELLOW") as pbar:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(process_symbol_wrapper, symbol, index): symbol for index, symbol in enumerate(symbols, start=1)}
                for index, future in enumerate(futures, start=1):
                    data, symbol, formatted_remaining_time = future.result()
                    if task_name == "Latest POS":
                        if data and "buy_date" in data["result"][2].keys():
                            buy_date_str = data["result"][2]["buy_date"]
                            buy_date = datetime.strptime(buy_date_str, "%Y-%m-%d")
                            if buy_date > latest_buy_date:
                                latest_buy_date = buy_date
                                best_pair = symbol
                                tab_best_pairs.append((best_pair, latest_buy_date.strftime("%Y-%m-%d")))
                            best_info = f"Best Pair: {best_pair} - Buy Date: {latest_buy_date.strftime('%Y-%m-%d')}"
                    elif task_name == "Biggest CR":
                        if data and "max_cumulative_ratio" in data["stats"]["positions"].keys():
                            cumulative_ratio = data["stats"]["positions"]["max_cumulative_ratio"]
                            if cumulative_ratio > max_cumulative_ratio:
                                max_cumulative_ratio = cumulative_ratio
                                best_pair = symbol
                                tab_best_pairs.append((best_pair, max_cumulative_ratio))
                            best_info = f"Best Pair: {best_pair} - CR: {max_cumulative_ratio}"

                    pbar.set_postfix({
                        'Symbol': symbol,
                        'Time left': formatted_remaining_time,
                        'Best Info': best_info
                    })
                    pbar.update(1)

        pbar.write(f"{Fore.YELLOW}{Style.BRIGHT}All tokens processed!")
        pbar.write(f"{Fore.WHITE}Best Pairs for this strategy: {Fore.YELLOW}{tab_best_pairs}")

    def run(self, task_name, timeframe, strategy, fetch_latest_data):
        print(f"{Fore.WHITE}{Style.BRIGHT}Strategy Scanner: {Fore.YELLOW}{strategy}\n{Fore.WHITE}Timeframe: {Fore.YELLOW}{timeframe}\n{Fore.WHITE}Task: {Fore.YELLOW}{task_name}\n{Fore.WHITE}Fetch Latest Data: {Fore.YELLOW}{fetch_latest_data}")
        symbols = self.load_symbols()
        if task_name == "Latest POS":
            self.process_symbols(symbols, timeframe, strategy, fetch_latest_data, self.analyze_symbol, "Latest POS")
        elif task_name == "Biggest CR":
            self.process_symbols(symbols, timeframe, strategy, fetch_latest_data, self.analyze_symbol, "Biggest CR")

def LatestPOSScanner(timeframe, strategy, fetch_latest_data):
    scanner = TokenScanner()
    scanner.run("Latest POS", timeframe, strategy, fetch_latest_data)

def BiggestCRScanner(timeframe, strategy, fetch_latest_data):
    scanner = TokenScanner()
    scanner.run("Biggest CR", timeframe, strategy, fetch_latest_data)
