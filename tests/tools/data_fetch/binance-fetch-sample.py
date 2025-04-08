import os
import sys
sys.path.append(os.getcwd())
from tools.data_fetch.binance.binance import BinanceAPI

binance_api = BinanceAPI()

symbols = [
    'BTC/USDC', 'ETH/USDC', 'BNB/USDC',
    'ADA/USDC', 'XRP/USDC', 'DOGE/USDC',
    'LTC/USDC', 'DOT/USDC', 'UNI/USDC',
    'LINK/USDC', 'LUNA/USDC',
    'SOL/USDC', 'AVAX/USDC',
    'MATIC/USDC', 'ATOM/USDC', 'XLM/USDC',
    'TRX/USDC',
    'AAVE/USDC'
]

binance_api.fetch_tokens_daily_ohlcv(symbols)