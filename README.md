# QTSBE - Quantitative Trading Strategy Backtesting Environment

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/logo.jpeg?raw=true" width="400" height="400">
</p>

QTSBE is an open-source project designed to provide a robust environment for backtesting quantitative trading strategies. It includes an API developed in Python using Flask and an interface built with Python.

<p align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white">
  <img src="https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white">
  <img src="https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white">
  <img src="https://img.shields.io/badge/Yahoo!-6001D2?style=for-the-badge&logo=Yahoo!&logoColor=white">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
</p>

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/white_2.png?raw=true" width="618.8" height="463.8">
</p>

## Features

- Backtesting environment for quantitative trading strategies. (Numpy / Pandas)
- API for strategy implementation and testing. (Flask)
- Visualization tools for strategy performance. (Plotly / Discord)
- Tools to fetch data. (from yfinance or Binance API).
- Tool to apply your trading strategy to a list of cryptos/stocks and see the stats of all. (Scanner)
- Test files to enhance developer usage.

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
     See others params in `api/README.md`

4. **Visualize Results (integrations):**
   
     - Use Plotly Chart representation:
    
       ```bash
       sh tests/integrations/plotly_unit.sh
       ```
  
     - Use discord bot and following commands:
    
       Configure the bot in `integrations/discord_chat_bot/bot.py`
    
       ```bash
       sh sh/discord_chat_bot.sh
       ```

5.  **Fetch your data properly:**
      Configure the file `tools/auto_fetch/config.json`using `tools/auto_fetch/README.md`
      - Using auto_fetch tool:

       ```bash
        sh sh/auto_fetch.sh
       ```

## Charts

![image](https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/white_3.png?raw=true)
![image](https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/black_2.png?raw=true)
![image](https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/void.png?raw=true)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

> [!CAUTION]  
> Always review the code before using it. The documentation or the purpose of the code may not be updated, so please check everything you use. 
> Developers are not responsible for any loss, miscalculation, or related issues resulting in losing money.

---

For questions or inquiries, feel free to contact me on [LinkedIn](https://www.linkedin.com).
