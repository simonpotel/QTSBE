### QTSBE/data

In this directory, we have the following components:

#### bank
This directory contains the data fetched by the API from Binance, organized by timeframe and trading pair.

#### binance_api.py
This module provides access to the Binance API. You can utilize its functions as follows:

```python
# Example usage: Fetch OHLCV data for the BTC/USDT trading pair at a 1-day interval and save it to a CSV file
BinanceAPI.fetch_and_save_ohlcv("BTC/USDT", "1d")
```

```python
# Example usage: Fetch the top 50 tokens by trading volume on Binance
BinanceAPI.get_top_50_tokens_by_volume()
```

```python
# Example usage: Fetch daily OHLCV data for the top 50 tokens by trading volume on Binance
BinanceAPI.fetch_tokens_daily_ohlcv(BinanceAPI.get_top_50_tokens_by_volume())
```

```python
# Example usage: Fetch the 100 most recent trading pairs that trade with TRY on Binance
BinanceAPI.get_recent_try_pairs()
```

```python
# Example usage: Fetch the 50 tokens with the least price variation over the past 15 days on Binance
BinanceAPI.get_least_volatile_tokens(15)
```

```python
# Example usage: Fetch the 50 tokens with the highest price variation over the past 2 days on Binance
BinanceAPI.get_most_volatile_tokens(2)
```

```python
# Example usage: Fetch and save OHLCV data for a custom trading pair and timeframe provided as command-line arguments
python binance_api.py -symbol "ETH/USDT" -timeframe "1h"
```

Please note that there are usage limits imposed by the Binance API. It allows a maximum of 600 requests per minute.

The data format within the `bank/` directory is currently CSV, and there are plans to update it to HDF5 format in the future for better efficiency.
