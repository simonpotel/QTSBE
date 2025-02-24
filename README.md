# QTSBE - Quantitative Trading Strategy Backtesting Environment

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/logo.jpeg?raw=true" width="400" height="400">
</p>

QTSBE is an open-source platform for backtesting quantitative trading strategies. It features a Python-based API built with Flask, offering multiple endpoints to facilitate seamless integration into existing projects.

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
  <img src="https://github.com/simonpotel/QTSBE/blob/365fd8b435958808fb084e1f998ca20fa599b04e/assets/smartswap.png">
</p>

## Key Features

- Comprehensive backtesting environment powered by NumPy and Pandas
- Flask-based API with caching system for optimized performance
- Interactive strategy visualization using Plotly
- Data integration with Yahoo Finance and Binance APIs
- Scanner tool for applying strategies across multiple cryptocurrencies and stocks
- Rich API endpoints for quick backtesting analysis and integration

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/simonpotel/QTSBE
   ```

2. Run the docker:
   ```bash
   docker-compose up
   ```

### Usage Guide

1. **Implement Your Strategy**
   - Use the template in `api/strategies/default.py` or refer to `api/strategies/rsi_example`
   - Create a new Python file with an `analyse` function that returns the required data
   - Implement indicators directly in your code without including them in the JSON response

2. **Launch the API**
   ```bash
   python api/api.py
   ```

3. **Available API Endpoints**
   - Get available tokens: `http://127.0.0.1:5000/QTSBE/get_tokens`
   - List strategies: `http://127.0.0.1:5000/QTSBE/get_strategies`
   - Run analysis: `http://127.0.0.1:5000/QTSBE/analyse`
   - Custom analysis: `http://127.0.0.1:5000/QTSBE/analyse_custom` (POST method)

   Note: Replace `127.0.0.1:5000` with your server's IP or domain name as needed on config.

4. **Visualization Options**
   - Generate Plotly charts:
     ```bash
     sh tests/integrations/plotly_unit.sh
     ```
   
   - Use the Discord bot:
     1. Configure settings in `integrations/discord_chat_bot/bot.py`
     2. Launch the bot:
        ```bash
        sh sh/discord_chat_bot.sh
        ```
   
   - Create custom interfaces (e.g., web interface) similar to the Smartswap project

5. **Data Collection**
   - Configure `tools/auto_fetch/config.json` following instructions in `tools/auto_fetch/README.md`
   - Run the auto-fetch tool:
     ```bash
     sh sh/auto_fetch.sh
     ```

## Builtin Visualization Plotly

![Example Chart 1](https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/white_3.png?raw=true)
![Example Chart 2](https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/black_2.png?raw=true)

## Projects Samples (here is what you can create using QTSBE)
- Automated trading bot that uses your strategy for live trading
- Dashboard to visualize your strategies with live data
- Alert system that notifies you of trading opportunities
- Scanner to find the best trading pairs for your strategy
- Tool to test and compare different trading strategies


## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Important Disclaimer

> [!CAUTION]  
> Please review all code thoroughly before implementation. Documentation and code purposes may not be current. The developers are not liable for any financial losses, calculation errors, or related issues that may occur from using this software.

---

For questions or support, connect with me on [LinkedIn](https://www.linkedin.com/in/simonpotel/).
