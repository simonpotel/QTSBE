# QTSBE - Quantitative Trading Strategy Backtesting Environment

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/logo.jpeg?raw=true" width="400" height="400">
</p>

QTSBE is a robust, open-source platform designed for backtesting quantitative trading strategies. At its core, it provides a powerful Python-based API built with Flask, offering extensive endpoints for seamless integration with existing trading systems and projects.

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

- **Advanced Backtesting Engine**: Powered by NumPy and Pandas for high-performance computations
- **Optimized API Architecture**: Flask-based with an intelligent caching system for superior performance
- **Dynamic Visualization**: Interactive strategy analysis using Plotly
- **Comprehensive Data Integration**: 
  - Real-time and historical data from Yahoo Finance
  - Cryptocurrency data through Binance API
- **Strategy Scanner**: Powerful tool for analyzing multiple assets simultaneously
- **Extensive API Ecosystem**: Rich set of endpoints for rapid strategy development and testing

## Quick Start Guide

### Installation

1. Clone the repository:
```bash
git clone https://github.com/simonpotel/QTSBE
```

2. Deploy with Docker:
```bash
docker-compose up
```

### Implementation Guide

1. **Strategy Development**
   - Base template: `api/strategies/default.py`
   - Example implementation: `api/strategies/rsi_example`
   - Create your strategy file with an `analyse` function
   - Implement technical indicators directly in your strategy code

2. **API Deployment**
```bash
python api/api.py
```

3. **API Documentation**
   - Access the Swagger UI documentation: `http://127.0.0.1:5002/docs`
   - Comprehensive endpoint documentation and testing interface

4. **Running Tests**
> [!TIP]
> Run fixtures of the API with : `pytest tests/test_api_endpoints.py`

5. **Visualization Tools**

   a. Generate Plotly Charts:
   ```bash
   sh tests/integrations/plotly_unit.sh
   ```
   
   b. Discord Integration:
   - Configure: `integrations/discord_chat_bot/bot.py`
   - Launch:
   ```bash
   sh sh/discord_chat_bot.sh
   ```
   
   c. Custom Interface Development
   - Framework available for building custom web interfaces
   - Reference the Smartswap project for implementation examples

6. **Automated Data Collection**
   - Configure: `tools/auto_fetch/config.json`
   - Launch collector:
   ```bash
   sh sh/auto_fetch.sh
   ```

## Visualization Examples

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/white_3.png?raw=true" width="100%">
  <img src="https://github.com/simonpotel/QTSBE/blob/master/assets/integration/plotly/black_2.png?raw=true" width="100%">
</p>

## Statistics Reference

| Section | Field | Goal | Analysis | Reference |
|---------|-------|------|---------------|-----------|
| Positions | average_ratio | Average ratio of individual positions. | > | https://www.investopedia.com/terms/r/returnoninvestment.asp |
| Positions | final_cumulative_ratio | Total compounded return across all positions. | > | https://www.investopedia.com/terms/c/cagr.asp |
| Positions | average_position_duration | Mean duration (days) a position is held. | ~ | https://www.investopedia.com/terms/h/holdingperiod.asp |
| Positions | lowest_ratio | Lowest single‐trade ratio. | > | |
| Positions | lowest_ratio_buy_index | Index of the trade with lowest ratio. | info | |
| Positions | lowest_ratio_sell_index | Index when lowest ratio trade closed. | info | |
| Positions | biggest_ratio | Highest single‐trade ratio. | > | https://www.investopedia.com/terms/r/return.asp |
| Positions | biggest_ratio_buy_index | Index of trade with highest ratio. | info | |
| Positions | biggest_ratio_sell_index | Index when highest ratio trade closed. | info | |
| Positions | biggest_position_duration | Longest trade duration (days). | ~ | https://www.investopedia.com/terms/h/holdingperiod.asp |
| Positions | lowest_position_duration | Shortest trade duration (days). | ~ | https://www.investopedia.com/terms/h/holdingperiod.asp |
| Positions | max_cumulative_ratio | Peak cumulative return. | > | https://www.investopedia.com/terms/c/cagr.asp |
| Positions | min_cumulative_ratio | Lowest cumulative return encountered. | > | |
| Positions | average_cumulative_ratio | Mean of cumulative return curve. | > | https://www.investopedia.com/terms/c/cagr.asp |
| Positions | lowest_cr_ratio | Lowest cumulative ratio reset value. | > | |
| Drawdown | max_drawdown | Worst peak‐to‐trough decline. | < | https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp |
| Drawdown | average_drawdown | Mean drawdown over the backtest. | < | https://www.investopedia.com/terms/d/drawdown.asp |
| Drawdown | max_drawdown_period | Dates of peak→trough for max DD. | < | https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp |
| Advanced | sharpe_ratio | Risk-adjusted return (σ). | > | https://www.investopedia.com/terms/s/sharperatio.asp |
| Advanced | sortino_ratio | Downside risk-adjusted return. | > | https://www.investopedia.com/terms/s/sortinoratio.asp |
| Advanced | volatility | Standard deviation of trade returns. | < | https://www.investopedia.com/terms/v/volatility.asp |
| Advanced | annualized_return | CAGR of the strategy. | > | https://www.investopedia.com/terms/c/cagr.asp |
| Advanced | calmar_ratio | Annualized return ÷ max drawdown. | > | https://www.investopedia.com/terms/c/calmarratio.asp |
| Advanced | recovery_factor | Final return ÷ max drawdown. | > | https://www.investopedia.com/terms/r/recovery-rate.asp |
| Advanced | win_rate | % of winning trades. | > | |
| Advanced | loss_rate | % of losing trades. | < | |
| Advanced | profit_factor | Gross profit ÷ gross loss. | > | |
| Advanced | expectancy | Average return per trade. | > | |
| Advanced | trade_frequency_per_year | Number of closed trades per year. | info | |
| Advanced | exposure_pct | % of time capital is exposed. | info | |
| Advanced | skewness | Asymmetry of return distribution. | ≈0 | https://www.investopedia.com/terms/s/skewness.asp |
| Advanced | kurtosis | Tail heaviness of returns. | ≈3 | https://www.investopedia.com/terms/k/kurtosis.asp |
| Advanced | VaR_95 | 5% worst-case daily return. | > | https://www.investopedia.com/terms/v/var.asp |
| Advanced | CVaR_95 | Average of worst 5% returns. | > | https://www.investopedia.com/terms/c/conditional_value_at_risk.asp |
| Advanced | consecutive_wins | Longest winning streak. | > | |
| Advanced | consecutive_losses | Longest losing streak. | < | |
| Advanced | max_drawdown_period_days | Days between peak and trough of max drawdown. | < | https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp |
| Advanced | time_to_recovery_days | Days needed to recover after max drawdown. | < | |

## Value Analysis Legend

- `>` : Higher value is better (maximize)
- `<` : Lower value is better (minimize)
- `≈0` : Value close to zero is ideal (neutral skewness)
- `≈3` : Value close to 3 is ideal (normal kurtosis)
- `~` : No optimal value, depends on strategy or context
- `info` : Informational only, not directly used for scoring

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Risk Disclaimer

> [!WARNING]  
> This software is provided for research and educational purposes only. Users should:
> - Thoroughly review and test all code before implementation
> - Be aware that documentation may not reflect the latest updates
> - Understand that the developers assume no liability for financial losses or calculation errors
> - Conduct their own risk assessment before using in live trading

---

For professional inquiries and support, connect with me on [LinkedIn](https://www.linkedin.com/in/simonpotel/).
