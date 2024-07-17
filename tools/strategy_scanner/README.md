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
from token_scanner import TokenScanner

scanner = TokenScanner()
timeframe = '1h'
strategy = 'strategy_name'
fetch_latest_data = True

scanner.scan(timeframe, strategy, fetch_latest_data)
```

#### Parameters

- `timeframe`: The timeframe for the OHLCV data (e.g., '1m', '5m', '1h', '1d').
- `strategy`: The trading strategy to apply.
- `fetch_latest_data`: Set to `True` to fetch the latest OHLCV data before analysis, or `False` to use existing data. Be careful with this parameter, dont use it too much, see `https://developers.binance.com/docs/derivatives/coin-margined-futures/error-code` -1003 TOO_MANY_REQUESTS#

### Output

The results are saved in a JSON file named `scan_result.json`, containing statistics for each pair and indicating the best pairs according to the chosen strategy.

