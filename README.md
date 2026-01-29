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
  <img src="https://img.shields.io/badge/pytest-%23C1E81C.svg?style=for-the-badge&logo=pytest&logoColor=black">
  <img src="https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white">
  <img src="https://img.shields.io/badge/Yahoo!-6001D2?style=for-the-badge&logo=Yahoo!&logoColor=white">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
</p>

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/365fd8b435958808fb084e1f998ca20fa599b04e/assets/smartswap.png">
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
   - Create your strategy file with required functions (`buy_signal`, `sell_signal`, `Indicators`)

2. **API Deployment**
```bash
python api/api.py
```

3. **API Documentation**
   - API Documentation is available via **Postman**.
   - Import the collection located in `docs/postman/QTSBE_API_Collection.json`.
   - See [Postman Documentation](docs/postman.md) for detailed instructions.

4. **Automated Data Collection**
   - Configure: `config/data_cron.json`
   - Launch collector: `python tools/data/cron.py`

## Documentation

For more detailed information, please refer to the following guides:

- [🚀 Strategy Development](docs/strategies.md) : How to build and add your own trading strategies.
- [⚙️ Configuration](docs/configuration.md) : Detailed explanation of all configuration files.
- [📊 Data Management](docs/data.md) : Understanding HDF5 storage and data structures.
- [🛠️ Tooling](docs/tools.md) : Overview of data fetching and maintenance tools.
- [📮 Postman Guide](docs/postman.md) : How to import and use the API collection.

## Testing

QTSBE uses **Pytest** for automated integration testing.

| Endpoint | Test Objective |
|----------|----------------|
| `/QTSBE/health` | Service health and external connectivity |
| `/QTSBE/get_tokens` | Listing of available HDF5 datasets |
| `/QTSBE/get_tokens_stats` | Live performance and metadata validation |
| `/QTSBE/get_strategies` | Discovery of local Python strategy modules |
| `/QTSBE/analyse` | Core backtesting engine execution |
| `/QTSBE/analyse_custom` | Dynamic execution of injected strategy code |

To run the tests simply execute:
```bash
pytest
```

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
