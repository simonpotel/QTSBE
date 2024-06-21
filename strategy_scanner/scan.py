from BinanceScanner.scanner import BinanceScanner

scanner = BinanceScanner()

specific_symbols = ['BTC/USDT', 
                    'ETH/USDT', 
                    'SOL/USDT', 
                    'DOGE/USDT',
                    'BNB/USDT',
                    'MATIC/USDT',
                    'AVAX/USDT',
                    'LUNA/USDT',
                    'XRP/USDT',
                    'LINK/USDT',
                    'RNDR/USDT',
                    'ADA/USDT',
                    'FTM/USDT',
                    'XTZ/USDT',
                    'SUI/USDT',
                    'SEI/USDT',
                    'NEAR/USDT',
                    'ARB/USDT',
                    'GRT/USDT',
                    'TRB/USDT',
                    'BAND/USDT',
                    'UNI/USDT',         
                    'SHIB/USDT',
                    'PEPE/USDT',
                    'TRX/USDT']
timeframe = '1d'
strategy = 'QTS_bollinger3_multi'
fetch_latest_data = True

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols)