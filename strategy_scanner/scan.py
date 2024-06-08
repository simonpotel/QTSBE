from scanner.main import *

TokenScanner().scan(timeframe='1d', 
            strategy='rsi_example', 
            fetch_latest_data=False)
