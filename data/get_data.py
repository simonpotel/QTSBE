from binance_api import BinanceAPI

BinanceAPI = BinanceAPI()
#BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_top_50_tokens_by_volume())
#BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_recent_try_pairs())
BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_least_volatile_tokens(15))