from tools.strategy_scanner.binance.scanner import BinanceScanner
scanner = BinanceScanner()

specific_symbols = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT',
    'ADA/USDT', 'XRP/USDT', 'DOGE/USDT',
    'LTC/USDT', 'DOT/USDT', 'UNI/USDT',
    'LINK/USDT', 'LUNA/USDT',
    'SOL/USDT', 'AVAX/USDT',
    'MATIC/USDT', 'ATOM/USDT', 'XLM/USDT',
    'TRX/USDT',
    'AAVE/USDT'
]

timeframe = '1d'
strategy = 'QTS_bollinger_lower_analyse'
fetch_latest_data = False

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols)