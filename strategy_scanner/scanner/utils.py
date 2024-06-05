from colorama import Fore

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} min {seconds} sec"

def print_progress(symbol, index, total_symbols, progress_percent, formatted_remaining_time):
    print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}{progress_percent:.2f}{Fore.WHITE}% complete ({Fore.YELLOW}Time left: {Fore.GREEN}{formatted_remaining_time}{Fore.WHITE})\r")

def print_analysis(symbol, index, total_symbols, cumulative_ratio):
    print(f"{Fore.LIGHTMAGENTA_EX}{symbol} {Fore.WHITE}({index}/{total_symbols}) - {Fore.GREEN}CR: {cumulative_ratio}{Fore.WHITE}\r")

def print_best_pair(best_pair, max_cumulative_ratio):
    print(f"{Fore.RED}Best Pair: ({best_pair}) - CR: {max_cumulative_ratio}\r")
