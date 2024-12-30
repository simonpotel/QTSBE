# Data

Storage and management of market data.

## Directory Structure

### /bank
Contains OHLCV data fetched from various providers:
- Binance
- Yahoo Finance
- Other supported providers

Data is organized by:
- Trading pair
- Timeframe
- Provider

## Data Fetching

See `tools/data_fetch` for:
- Fetching new data
- Updating existing data
- Supported providers and pairs

## Format

Data is stored in CSV format with columns:
- timestamp
- open
- high
- low
- close
- volume