# api/

This directory contains all the code for the API, including the algorithmic logic, statistical system, and all the strategies utilized by the API.

#### Getting Started
To start the Flask API, navigate to the QTSBE directory and run the following command:

```bash
python api/api.py
```

You can now make requests via your web browser:

```bash
http://127.0.0.1:5000/QTSBE/<pair>/<strategy>
```

For example:

```bash
http://127.0.0.1:5000/QTSBE/Binance_BTCUSDT_1d/default
```

You can also use the tool in QTSBE/display/python/main.py

#### API parameters
- **`start_ts`**: Date format should be "%Y-%m-%d %H:%M:%S", for example, '2000-01-01 00:00:00'.
- **`end_ts`**: Date format should be "%Y-%m-%d %H:%M:%S", for example, '2000-01-01 00:00:00'.
- **`multi_positions`**: This parameter should be set to True or False. It determines whether your strategy allows multiple positions to be open simultaneously.
- **`details`**: This parameter should be set to True or False. When set to True, it indicates that you want to retrieve detailed information such as OHLCV (Open, High, Low, Close, Volume) data from data/bank files and values of indicators. Setting it to False can improve the speed of your code, especially useful when using a real-time simulator. However, if you intend to create graphs and plot different curves, you must set `details` to True to obtain the necessary data.

