import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.binance.binance_api import BinanceAPI

binance_api = BinanceAPI()

symbols = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
    'ADA/USDT', 'XRP/USDT', 'DOGE/USDT',
    'LTC/USDT', 'DOT/USDT', 'UNI/USDT',
    'LINK/USDT', 'LUNA/USDT',
    'SOL/USDT', 'AVAX/USDT',
    'MATIC/USDT', 'ATOM/USDT', 'XLM/USDT',
    'TRX/USDT',
    'AAVE/USDT'
]

binance_api.fetch_tokens_daily_ohlcv(symbols)