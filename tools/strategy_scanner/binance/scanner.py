import sys
import os
from colorama import init, Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm
import json
import math

#sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data'))
#from binance_api import BinanceAPI
from tools.data_fetch.binance.binance import BinanceAPI

init(autoreset=True)

def format_time(seconds):
    minutes = math.floor(seconds / 60)
    seconds = math.ceil(seconds % 60)
    return f"{minutes}m {seconds}s"

class BinanceScanner(object):
    def __init__(self):
        self.binance = BinanceAPI()

    def load_symbols(self):
        return self.binance.exchange.load_markets()

    def analyze_symbol(self, symbol, timeframe, strategy):
        url = f"http://127.0.0.1:5000/QTSBE/Binance_{symbol.replace('/', '')}_{timeframe}/{strategy}"
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Invalid JSON response for {symbol}: {response.text}")
            return {}  # Return an empty dictionary or handle as appropriate

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

        drawdowns = []
        positions_ratios = []

        with tqdm(total=total_symbols, desc="Processing scan", unit="symbol", ncols=100, dynamic_ncols=True, colour="BLUE") as pbar:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(process_symbol_wrapper, symbol, index): symbol for index, symbol in enumerate(symbols, start=1)}
                for index, future in enumerate(futures, start=1):
                    data, symbol, formatted_remaining_time = future.result()
                    if data != {}:
                        if data and "stats" in data:
                            stats = data["stats"]
                            all_stats.append((symbol, stats, data))
                            if "drawdown:" in stats:
                                drawdowns.append((symbol, stats["drawdown:"]))
                            elif "drawdowns" in stats:
                                drawdowns.append((symbol, stats["drawdowns"]))
                            if "positions" in stats and "max_cumulative_ratio" in stats["positions"]:
                                positions_ratios.append((symbol, stats["positions"]["max_cumulative_ratio"]))

                    pbar.set_postfix({
                        'Symbol': symbol,
                        'Time left': formatted_remaining_time,
                    })
                    pbar.update(1)

        pbar.write(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}All tokens processed!")
        all_stats_sorted = sorted(all_stats, key=lambda x: x[1]["positions"]["max_cumulative_ratio"], reverse=True)
        self.save_stats_to_json(all_stats_sorted)
        self.save_global_stats_to_json(drawdowns, positions_ratios)

    def save_stats_to_json(self, all_stats):
        result = {"tokens": []}
        for symbol, _, data in all_stats:
            result["tokens"].append({
                "symbol": symbol,
                "data": data
            })
        with open('scan_result.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Results saved to scan_result.json")


    def save_global_stats_to_json(self, drawdowns, positions_ratios):
        if drawdowns:
            drawdowns_sorted = sorted(drawdowns, key=lambda x: x[1]["max_drawdown"], reverse=True)
            max_drawdown = drawdowns_sorted[0]
            min_drawdown = drawdowns_sorted[-1]
            avg_drawdown = sum(dd[1]["max_drawdown"] for dd in drawdowns) / len(drawdowns)
            max_drawdown_period = max(drawdowns, key=lambda x: x[1]["max_drawdown_period"])
        else:
            max_drawdown = ("N/A", {"max_drawdown": 0})
            min_drawdown = ("N/A", {"max_drawdown": 0})
            avg_drawdown = 0
            max_drawdown_period = ("N/A", {"max_drawdown_period": 0})

        if positions_ratios:
            positions_ratios_sorted = sorted(positions_ratios, key=lambda x: x[1], reverse=True)
            avg_ratio_cr = sum(pr[1] for pr in positions_ratios) / len(positions_ratios)
            max_ratio_cr = positions_ratios_sorted[0]
            min_ratio_cr = positions_ratios_sorted[-1]
        else:
            avg_ratio_cr = 0
            max_ratio_cr = ("N/A", 0)
            min_ratio_cr = ("N/A", 0)

        global_stats = {
            "drawdowns": {
                "max_drawdown": max_drawdown[1]["max_drawdown"],
                "max_drawdown_pair": max_drawdown[0],
                "min_drawdown": min_drawdown[1]["max_drawdown"],
                "min_drawdown_pair": min_drawdown[0],
                "average_drawdown": avg_drawdown,
                "max_drawdown_period": max_drawdown_period[1]["max_drawdown_period"],
                "max_drawdown_period_pair": max_drawdown_period[0],
            },
            "positions": {
                "avg_ratio_cr": avg_ratio_cr,
                "max_ratio_cr": max_ratio_cr[1],
                "max_ratio_cr_pair": max_ratio_cr[0],
                "min_ratio_cr": min_ratio_cr[1],
                "min_ratio_cr_pair": min_ratio_cr[0]
            }
        }

        with open('global_stats.json', 'w') as json_file:
            json.dump(global_stats, json_file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Global statistics saved to global_stats.json")

    def scan(self, timeframe, strategy, fetch_latest_data, symbols=None):
        print(f"{Fore.WHITE}{Style.BRIGHT}Strategy Scanner: {Fore.LIGHTBLUE_EX}{strategy}\n{Fore.WHITE}Timeframe: {Fore.LIGHTBLUE_EX}{timeframe}\n{Fore.WHITE}Fetch Latest Data: {Fore.LIGHTBLUE_EX}{fetch_latest_data}")
        if symbols is None:
            symbols = self.load_symbols()
        self.process_symbols(symbols, timeframe, strategy, fetch_latest_data, self.analyze_symbol)

    def rank_symbols_by_recent_buy_date(self, timeframe, strategy, symbols=None):
        print(f"{Fore.WHITE}{Style.BRIGHT}Ranking Symbols by Most Recent Buy Date for Strategy: {Fore.LIGHTBLUE_EX}{strategy}\n{Fore.WHITE}Timeframe: {Fore.LIGHTBLUE_EX}{timeframe}")
        if symbols is None:
            symbols = self.load_symbols()

        def analyze_and_get_recent_buy_date(symbol):
            data = self.analyze_symbol(symbol, timeframe, strategy)
            if data and "result" in data and len(data["result"]) >= 3:
                result = data["result"][2]
                if result and "buy_date" in result:
                    return result["buy_date"], symbol
            return None

        valid_symbols = []
        with ThreadPoolExecutor(max_workers=7) as executor:
            futures = {executor.submit(analyze_and_get_recent_buy_date, symbol): symbol for symbol in symbols}
            for index, future in enumerate(futures):
                result = future.result()
                if result:
                    print(result, str(index)+"/"+str(len(futures)))
                    valid_symbols.append(result)

        print(" ")
        ranked_symbols = sorted(valid_symbols, key=lambda x: x[0], reverse=True)
        return ranked_symbols
