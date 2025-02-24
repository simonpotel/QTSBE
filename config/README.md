# Configuration Files Documentation

## api.json

``` json
{
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
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

## auto_fetch.json

``` json
{
{
    "Yahoo": [
        ["AAPL", "1d"]
    ],
    "Binance": [
        ["BTC/USDT", "1d"],
        ["ETH/USDT", "1d"]
    ]
}
}
```
