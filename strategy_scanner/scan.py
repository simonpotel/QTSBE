from BinanceScanner.scanner import BinanceScanner
scanner = BinanceScanner()

specific_symbols = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
    'ADA/USDT', 'XRP/USDT', 'DOGE/USDT',
    'LTC/USDT', 'DOT/USDT', 'UNI/USDT',
    'LINK/USDT', 'BCH/USDT', 'LUNA/USDT',
    'SOL/USDT', 'AVAX/USDT', 'ALGO/USDT',
    'VET/USDT', 'FIL/USDT', 'ICP/USDT',
    'MATIC/USDT', 'ATOM/USDT', 'XLM/USDT',
    'TRX/USDT', 'ETC/USDT', 'FTT/USDT',
    'THETA/USDT', 'XTZ/USDT', 'EOS/USDT',
    'AAVE/USDT', 'KSM/USDT', 'NEO/USDT',
    'MKR/USDT', 'CAKE/USDT', 'COMP/USDT',
    'ENJ/USDT', 'ZEC/USDT', 'DASH/USDT',
    'MANA/USDT', 'ZIL/USDT', 'CHZ/USDT',
    'SAND/USDT', 'AXS/USDT'
]

timeframe = '1d'
strategy = 'default'
fetch_latest_data = True

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols)