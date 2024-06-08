from BinanceScanner.scanner import BinanceScanner

BinanceScanner().scan(timeframe='1d', 
            strategy='rsi_example', 
            fetch_latest_data=False)
