# QTSBE - Quantitative Trading Strategy Backtesting Environment

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/ed041293f294cd7a9caeff7c55f4baa0c3e93c61/files/logo.jpeg" width="400" height="400">
</p>

QTSBE is an open-source project aimed at providing a robust environment for backtesting quantitative trading strategies. It includes an API developed in Python using Flask and an interface built with Python.

<p align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Blockchain.com-121D33?logo=blockchaindotcom&logoColor=fff&style=for-the-badge"> 
  <img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white">
</p>

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/dev_doc/assets/integration/plotly/white_2.png?raw=true" width="618.8" height="463.8">
</p>


## Features

- Comprehensive backtesting environment for quantitative trading strategies.
- API for strategy implementation and testing.
- Visualization tools for strategy performance.
- Tool to fetch datas (from yfinance or Binance api)
- Tool to apply your trading strategy to a list of cryptos/stck and see the stats of all in 5 seconds
- Tests files to enhance developer usage
- Easy customization of charts (plotly), indicators functions and strategies.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/simonpotel/QTSBE
   ```

2. Install dependencies:

   ```bash
   cd QTSBE
   pip install -r requirements.txt
   ```

### Usage

1. **Create Your Strategy:**
   - Create your strategy based on the default structure found in `api/strategies/default.py`, or use the simple base example in `api/strategies/rsi_example`.
   - Implement your strategy by creating a new Python file and defining the `analyse` function that returns the required data. You can choose to use indicators within the code without passing them in the JSON response.

2. **Start the API:**
   - Run the API using `api/api.py`.

   ```bash
   python api/api.py
   ```

3. **Access the API:**
   - Get the API response in your web browser: `http://127.0.0.1:5000/QTSBE/<data_set>/<your_strategy_name>`.

4. **Visualize Results:**
   - Start the GUI for visualizing the API response by running `integration/plotly/main.py`.

   ```bash
   integration/plotly/main.py -data 'Binance_BTCUSDT_1d' -strategy 'rsi_example' -multi_positions False
   ```

   - The display tool allows you to select your strategy and the dataset to apply it to.
   
## Customization
![image](https://github.com/simonpotel/QTSBE/blob/dev_doc/assets/integration/plotly/white_3.png?raw=true)
![image](https://github.com/simonpotel/QTSBE/blob/dev_doc/assets/integration/plotly/black_2.png?raw=true)
![image](https://github.com/simonpotel/QTSBE/blob/dev_doc/assets/integration/plotly/void.png?raw=true)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Note: The contents of the files in the indicators folder are not guaranteed to be completely accurate. Always review the code of each indicator before use.

---

For questions or inquiries, feel free to contact me on [LinkedIn](https://www.linkedin.com).
