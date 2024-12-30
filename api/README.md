# API

This directory contains the core API implementation, including algorithmic logic, statistical systems, and strategy management.

## Getting Started

Start the Flask API from the QTSBE root directory:

```bash
python api/api.py
```

## Usage

Make requests via web browser:

```bash
http://127.0.0.1:5000/QTSBE/<pair>/<strategy>
```

### Parameters

- **`pair`**: Trading pair (e.g., "Binance_BTCUSDT_1d")
- **`strategy`**: Strategy name to use (e.g., "default", "rsi_example")
- **`start_ts`**: Start timestamp in format "YYYY-MM-DD HH:MM:SS" (e.g., '2000-01-01 00:00:00')
- **`end_ts`**: End timestamp in format "YYYY-MM-DD HH:MM:SS"
- **`multi_positions`**: Allow multiple concurrent positions (true/false)
- **`details`**: Include full OHLCV data and indicators in response (true/false)
  - Set to true for plotting/visualization
  - Set to false for faster performance in real-time simulations

### Example

```bash
http://127.0.0.1:5000/QTSBE/Binance_BTCUSDT_1d/default?start_ts=2023-01-01%2000:00:00&multi_positions=false
```

## Directory Structure

- `/logs` - API logs and debugging information
- `/stats` - Statistical calculation modules
- `/strategies` - Trading strategy implementations

## Tools

You can also use the visualization tool at `QTSBE/display/python/main.py`

