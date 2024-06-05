### QTSBE/api

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

#### Debug Mode
You can start the API in debug mode to access debugging information. 

#### Logs
Logs for the API can be found in the following directory:

```
QTSBE/logs/
```

Feel free to explore and analyze the logs for further insight into the API's behavior.

### QTSBE/api/algo
This directory houses all the algorithmic code utilized within the API.

#### Data Retrieval
The `api/algo/data/file.py` module enables the retrieval of data for the desired trading pair from the API request in the database.

#### Indicators
The `api/algo/indicators` directory contains all the indicators used for technical analysis. As a technical choice, I've opted not to import another library and have developed them from scratch.
Feel free to explore the code for further understanding of the algorithmic processes and data handling within the API.

### QTSBE/api/stats

This directory facilitates the management of positions, trades, and automates the calculation of statistics on the positions executed within our strategies, providing better visibility.

#### QTSBE/api/stats/trades.py
This module manages trades using the following construction:

```python
add_trade(
    self,
    buy_index,
    buy_price,
    buy_date,
    buy_signals,
    sell_index,
    sell_price,
    sell_date,
    sell_signals
)
```

#### QTSBE/api/stats/positions.py
The `positions.py` module provides statistics such as:

- **max_loss:** Maximum loss incurred.
- **max_loss_buy_index:** Index at which the maximum loss occurred (at the buy stage).
- **max_loss_sell_index:** Index at which the maximum loss occurred (at the sell stage).
- **average_ratio:** Average profit/loss ratio.
- **all_ratios:** Ratios for all positions.
- **cumulative_ratios:** Cumulative ratios of profits/losses.
- **max_cumulative_ratio:** Maximum cumulative ratio achieved.
- **daily_average_ratio:** Average ratio on a daily basis.
- **hourly_average_ratio:** Average ratio on an hourly basis.
- **average_position_duration:** Average duration of positions.

#### QTSBE/api/stats/drawdown.py
The `drawdown.py` module calculates risk statistics including:

- **max_drawdown:** Largest percentage loss from a peak to a trough.
- **total_drawdown:** Cumulative sum of all individual drawdowns.
- **stability_ratio:** Efficiency of returns relative to the worst drawdown.
- **max_drawdown_period:** Period during which the maximum drawdown occurred.
- **average_drawdown:** Average drawdown across all positions.

### QTSBE/api/strategies

This directory, along with its subdirectories, serves as the repository for all Python files considered as strategies for the API. These strategies are loaded and utilized by the API.

To understand the structure of a strategy, you can refer to an example file such as `strategies/default.py`.

For private work environments, you can create a private repository and clone it into this `strategies` directory. Your cloned subdirectory and all your strategies will be loaded, ensuring privacy and confidentiality, and they will not be visible for open-source coding.

Each strategy follows the same function structure:

```python
def analyse(data, prices):
    """
    Analyzes the provided data and prices to make trading decisions.

    Parameters:
    - data: Data required for analysis.
    - prices: Price data for the trading pair.

    Returns:
    - positions: Object of the Positions class (via QTSBE/api/stats/trades.py).
    """
    # Your strategy implementation goes here
```

Ensure that your strategy function returns an object of the `positions` class, as defined in `QTSBE/api/stats/trades.py`.


