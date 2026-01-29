# Data Management

Storage and management of market data using the HDF5 format for high performance.

## Storage Location: `/data/bank`

All OHLCV data is stored in a single binary file:
- `data/bank/qtsbe_data.h5`

## Data Structure

Data is organized using keys within the HDF5 file. Keys follow the naming convention:
`{Provider}_{Pair}_{Timeframe}`

Examples:
- `Binance_BTCUSDC_1d`
- `Yahoo_AAPL_1h`

## Data Format

Each dataset is a matrix with 6 columns:
1. **timestamp**: Unix timestamp in milliseconds
2. **open**: Opening price
3. **high**: Highest price
4. **low**: Lowest price
5. **close**: Closing price
6. **volume**: Trading volume

## Data Fetching

Automation is handled by the `tools/data/cron.py` script.
Configuration is defined in `config/data_cron.json`.