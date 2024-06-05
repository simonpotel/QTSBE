### QTSBE/data

In this directory, we have the following components:

#### bank
This directory contains the data fetched by the API from Binance, organized by timeframe and trading pair.

#### binance_api.py
This module provides access to the Binance API. You can utilize its functions as follows:

```python
from binance_api import BinanceAPI

BinanceAPI = BinanceAPI()
# Example usage:
# BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_top_50_tokens_by_volume())
# BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_recent_try_pairs())
# BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_least_volatile_tokens(15))
# BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_most_volatile_tokens(2))
# BinanceAPI.fetch_and_save_ohlcv("BTCUSDT", "1d")
```

Please note that there are usage limits imposed by the Binance API. It allows a maximum of 600 requests per minute.

The data format within the `bank/` directory is currently CSV, and there are plans to update it to HDF5 format in the future for better efficiency.
