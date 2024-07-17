from tools.strategy_scanner.binance.scanner import BinanceScanner
scanner = BinanceScanner()

specific_symbols = [
    'BTC/USDT', 'ETH/USDT'
]

timeframe = '1d'
strategy = 'rsi_example'
fetch_latest_data = True

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols)