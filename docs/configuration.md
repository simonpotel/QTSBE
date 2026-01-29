# Configuration Files Documentation

## api.json

``` json
{
    "server": {
        "host": "0.0.0.0",
        "port": 5002,
        "debug": false
    },
    "cors": {
        "origins": [
            "http://127.0.0.1:1337",
            "http://localhost:1337"
        ]
    },
    "cache": {
        "type": "simple",
        "default_timeout": 300
    }
} 
```

## data_cron.json

``` json
{
{
    "Yahoo": [
        ["AAPL", "1d"]
    ],
    "Binance": [
        ["BTC/USDC", "1d"],
        ["ETH/USDC", "1d"]
    ]
}
}
```
