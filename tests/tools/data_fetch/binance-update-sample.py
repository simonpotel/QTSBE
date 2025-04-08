import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.binance.binance import BinanceAPI

binance_api = BinanceAPI()

symbols = [
    'BTC/USDC', 'SOL/USDC'
]

binance_api.update_ohlcv_for_symbols(symbols)