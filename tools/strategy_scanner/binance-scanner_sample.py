import os
import sys
sys.path.append(os.getcwd())
from tools.strategy_scanner.binance.scanner import BinanceScanner

scanner = BinanceScanner()

specific_symbols = [
    'BTC/USDT', 'ETH/USDT'
]

timeframe = '1d'
strategy = 'QTS_fibo'
fetch_latest_data = False
start_ts = '2024-01-01 00:00:00'
end_ts = '2025-01-01 00:00:00'

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols, start_ts=start_ts, end_ts=end_ts)