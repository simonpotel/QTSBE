import os
import time
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from colorama import Fore, Style
from tools.data_fetch.binance.binance import BinanceAPI

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"

class BinanceScanner(object):
    def __init__(self):
        self.binance = BinanceAPI()

    def load_symbols(self):
        return self.binance.exchange.load_markets()

    def analyze_symbol(self, symbol, timeframe, strategy, start_ts=None, end_ts=None):
        url = f"http://127.0.0.1:5000/QTSBE/Binance_{symbol.replace('/', '')}_{timeframe}/{strategy}"
        if start_ts or end_ts:
            url += "?"
        if start_ts:
            url += f"start_ts={start_ts}"
        if end_ts:  
            if start_ts:
                url += "&"
            url += f"end_ts={end_ts}"
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Invalid JSON response for {symbol}: {response.text}")
            return {}  # Return an empty dictionary or handle as appropriate

    def process_symbol(self, symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func, start_ts=None, end_ts=None):
        elapsed_time = time.time() - start_time
        avg_time_per_token = elapsed_time / index
        remaining_time = avg_time_per_token * (total_symbols - index)
        formatted_remaining_time = format_time(remaining_time)

        data = analysis_func(symbol, timeframe, strategy, start_ts, end_ts)
        return data, symbol, formatted_remaining_time

    def process_symbols(self, symbols, timeframe, strategy, fetch_latest_data, analysis_func, start_ts=None, end_ts=None):
        total_symbols = len(symbols)
        start_time = time.time()
        all_stats = []

        def process_symbol_wrapper(symbol, index):
            return self.process_symbol(symbol, index, total_symbols, start_time, timeframe, strategy, analysis_func, start_ts, end_ts)

        if fetch_latest_data:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(self.binance.fetch_and_save_ohlcv, symbol, timeframe): symbol for symbol in symbols}
                print(f"{Fore.LIGHTMAGENTA_EX}Fetching and saving OHLCV data for all tokens...\r")
                for future in futures:
                    future.result()  

        positions_stats = []
        with tqdm(total=total_symbols, desc="Processing scan", unit="symbol", ncols=100, dynamic_ncols=True, colour="BLUE") as pbar:
            with ThreadPoolExecutor(max_workers=7) as executor:
                futures = {executor.submit(process_symbol_wrapper, symbol, index): symbol for index, symbol in enumerate(symbols, start=1)}
                for index, future in enumerate(futures, start=1):
                    data, symbol, formatted_remaining_time = future.result()
                    if data != {}:
                        if data and "stats" in data:
                            stats = data["stats"]
                            all_stats.append((symbol, stats, data))
                            if "positions" in stats:
                                positions_stats.append((symbol, stats))
                    pbar.set_postfix({
                        'Symbol': symbol,
                        'Time left': formatted_remaining_time,
                    })
                    pbar.update(1)

        pbar.write(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}All tokens processed!")
        all_stats_sorted = sorted(all_stats, key=lambda x: x[1]["positions"]["max_cumulative_ratio"], reverse=True)
        self.save_stats_to_json(all_stats_sorted, strategy, start_ts, end_ts)
        self.save_global_stats_to_json(positions_stats, strategy, start_ts, end_ts)

    def save_stats_to_json(self, all_stats, strategy, start_ts, end_ts):
        result = {"tokens": []}
        for symbol, _, data in all_stats:
            result["tokens"].append({
                "symbol": symbol,
                "data": data
            })
        date_str = datetime.now().strftime("%Y%m%d")
        directory = f'tools/strategy_scanner/_results/binance_{strategy}-{date_str}-{start_ts}-{end_ts}'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, 'scan_results.json')
        with open(file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Results saved to {file_path}")
    
    def save_global_stats_to_json(self, positions_stats, strategy, start_ts, end_ts):
        global_stats = {
            "positions": {
                "all_ratios": [],
                "average_position_duration": 0,
                "average_ratio": 0,
                "biggest_position_duration": 0,
                "biggest_ratio": 0,
                "biggest_ratio_symbol": None,
                "lowest_position_duration": 0,
                "lowest_ratio": 0,
                "lowest_ratio_symbol": None,
                "percent_above_1_ratio": 0,
                "percent_below_1_ratio": 0,
                "max_cumulative_ratio": 0,
                "max_cumulative_symbol": None,
                "min_cumulative_ratio": 0,
                "min_cumulative_symbol": None,
                "average_cumulative_ratio": 0,
                "total_signals": 0,
                "average_signals": {},
                "yearly_best_symbol": {},
                "yearly_worst_symbol": {},
                "yearly_averages": {}
            }
        }
        if positions_stats:
            all_ratios = []
            cumulative_ratios = []
            durations = []
            buy_signals_count = {}
            sell_signals_count = {}
            yearly_data = {}
            total_signals = 0

            for symbol, stats in positions_stats:
                ratios = stats["positions"].get("all_ratios", [])
                all_ratios.extend(ratios)
                cumulative_ratios.append(stats["positions"].get("max_cumulative_ratio", 0))
                durations.append(stats["positions"].get("biggest_position_duration", 0))

                for key, value in stats["positions"].get("buy_signals_count", {}).items():
                    buy_signals_count[key] = buy_signals_count.get(key, 0) + value
                    total_signals += value
                for key, value in stats["positions"].get("sell_signals_count", {}).items():
                    sell_signals_count[key] = sell_signals_count.get(key, 0) + value
                    total_signals += value

                for year, ratio in stats["positions"].get("yearly_ratio", {}).items():
                    if year not in yearly_data:
                        yearly_data[year] = []
                    yearly_data[year].append((symbol, ratio))

            above_1 = sum(1 for r in all_ratios if r > 1)
            below_1 = sum(1 for r in all_ratios if r <= 1)
            global_stats["positions"]["all_ratios"] = all_ratios
            global_stats["positions"]["percent_above_1_ratio"] = (above_1 / len(all_ratios) * 100) if all_ratios else 0
            global_stats["positions"]["percent_below_1_ratio"] = (below_1 / len(all_ratios) * 100) if all_ratios else 0
            global_stats["positions"]["average_ratio"] = sum(all_ratios) / len(all_ratios) if all_ratios else 0
            global_stats["positions"]["biggest_ratio"] = max(all_ratios) if all_ratios else 0
            global_stats["positions"]["lowest_ratio"] = min(all_ratios) if all_ratios else 0
            global_stats["positions"]["biggest_ratio_symbol"] = max(positions_stats, key=lambda x: max(x[1]["positions"].get("all_ratios", [0])) if x[1]["positions"].get("all_ratios") else 0)[0]
            global_stats["positions"]["lowest_ratio_symbol"] = min(positions_stats, key=lambda x: min(x[1]["positions"].get("all_ratios", [float('inf')])) if x[1]["positions"].get("all_ratios") else float('inf'))[0]

            global_stats["positions"]["average_position_duration"] = sum(durations) / len(durations) if durations else 0
            global_stats["positions"]["biggest_position_duration"] = max(durations) if durations else 0

            global_stats["positions"]["max_cumulative_ratio"] = max(cumulative_ratios) if cumulative_ratios else 0
            global_stats["positions"]["min_cumulative_ratio"] = min(cumulative_ratios) if cumulative_ratios else 0
            global_stats["positions"]["max_cumulative_symbol"] = max(positions_stats, key=lambda x: x[1]["positions"].get("max_cumulative_ratio", 0))[0]
            global_stats["positions"]["min_cumulative_symbol"] = min(positions_stats, key=lambda x: x[1]["positions"].get("max_cumulative_ratio", float('inf')))[0]
            global_stats["positions"]["average_cumulative_ratio"] = sum(cumulative_ratios) / len(cumulative_ratios) if cumulative_ratios else 0

            global_stats["positions"]["total_signals"] = total_signals
            total_signal_types = {**buy_signals_count, **sell_signals_count}
            for signal, count in total_signal_types.items():
                global_stats["positions"]["average_signals"][signal] = count / len(positions_stats)

            for year, data in yearly_data.items():
                best_symbol = max(data, key=lambda x: x[1])[0]
                worst_symbol = min(data, key=lambda x: x[1])[0]
                average_yearly_ratio = sum(ratio for _, ratio in data) / len(data)
                global_stats["positions"]["yearly_best_symbol"][year] = best_symbol
                global_stats["positions"]["yearly_worst_symbol"][year] = worst_symbol
                global_stats["positions"]["yearly_averages"][year] = average_yearly_ratio

        date_str = datetime.now().strftime("%Y%m%d")
        directory = f'tools/strategy_scanner/_results/binance_{strategy}-{date_str}-{start_ts}-{end_ts}'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, 'global_stats.json')
        with open(file_path, 'w') as json_file:
            json.dump(global_stats, json_file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}Global statistics saved to {file_path}")
    
    def scan(self, timeframe, strategy, fetch_latest_data, symbols=None, start_ts=None, end_ts=None):
        print(f"{Fore.WHITE}{Style.BRIGHT}Strategy Scanner: {Fore.LIGHTBLUE_EX}{strategy}\n{Fore.WHITE}Timeframe: {Fore.LIGHTBLUE_EX}{timeframe}\n{Fore.WHITE}Fetch Latest Data: {Fore.LIGHTBLUE_EX}{fetch_latest_data}")
        if symbols is None:
            symbols = self.load_symbols()
        self.process_symbols(symbols, timeframe, strategy, fetch_latest_data, self.analyze_symbol, start_ts, end_ts)

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
