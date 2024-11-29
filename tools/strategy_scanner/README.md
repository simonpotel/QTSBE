## Binance Strategy Scanner

This folder contains an algorithm designed to scan all pairs on Binance exchange based on a given strategy and generate statistics on the best pairs to take positions according to this strategy.

### Overview

The algorithm utilizes Binance API to fetch data for all available trading pairs. It then applies the specified strategy to each pair and calculates relevant statistics to identify the most promising pairs.

### Options

- **Fetch Latest Data**: The scanner can optionally fetch the latest OHLCV data for all trading pairs before performing the analysis. This ensures that the analysis is based on the most recent market data.
- **Multithreaded Processing**: Uses multithreading to speed up the data fetching and analysis process. -> Be aware of this in `ThreadPoolExecutor(max_workers=7)`, if you put a large number, your processor will be done.

### Usage

#### Scan Tokens

To scan tokens with the option to fetch the latest data: (with scan.py)

```python
scanner = BinanceScanner()

specific_symbols = [
    "BTC/USDT",
    "ETH/USDT"]

timeframe = '1d'
strategy = 'rsi_example'
fetch_latest_data = True
start_ts = '2020-01-01 00:00:00'
end_ts = '2021-01-01 00:00:00'

scanner.scan(timeframe, strategy, fetch_latest_data, symbols=specific_symbols, start_ts=start_ts, end_ts=end_ts)

### Output

Results are saved in `tools/strategy_scanner/_results` with `binance_`prefix.