# Auto Fetch

Automated data fetching and updating tool.

## Configuration

Create `config.json` in this directory:

```json
{
    "Yahoo": [
        ["AMZN", "1d"],
        ["TSLA", "1d"],
        ["NKE", "1d"]
    ],
    "Binance": [
        ["BTC/USDT", "1d"],
        ["ETH/USDT", "1d"],
        ["SOL/USDT", "1d"]
    ]
}
```

## Features

- Automated data updates
- Multiple provider support
- Configurable pairs and timeframes
- Logging system

## Logs

Logs are stored in `logs/` directory:
- Daily rotation
- 7-day retention
- Error tracking
- Success monitoring

## Usage

Run with the provided shell script:

```bash
sh sh/auto_fetch.sh
```

