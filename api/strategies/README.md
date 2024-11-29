# api/strategies/

This folder contains all the strategies that will be loaded by the API.
All Python files in this folder and its subfolders will be loaded.

The best way to import your strategies is to create a private repository and clone it here as a folder.
Then, the files in the folder will be loaded.

From these Python files, the `Indicators` class, `buy_signal`, and `sell_signal` functions will be imported.

You must define these three requirements as follows:

The `Indicators` class should be defined like this:
```python
class Indicators(object):
    def __init__(self, data):
        self.data = data
        self.indicators = self.calculate_indicators()

    def calculate_indicators(self):
        data_open = [row[1] for row in the data]

        indicators = {
            "RSI": get_RSI(data_open),
        }
        return {k: list(v) for k, v in indicators.items()}
```
You can access the indicators using `object.indicators` and `object.indicators['RSI'][index_check]`.

The `buy_signal` function should have the following parameters:
```python
def buy_signal(open_position, data, index_check, indicators, current_price=None):
```
The `sell_signal` function should have the following parameters:
```python
def sell_signal(open_position, data, index_check, indicators, current_price=None):
```

`current_price` should be `None` during backtesting. If you use the strategy in a live automated trading program, you should set `current_price` with the price fetched from the broker.

Both `buy_signal` and `sell_signal` functions must return the signal and the price of the buy or sell action.
If you do not want to return anything, you should return `0, None`.
