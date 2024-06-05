# QTSBE - Quantitative Trading Strategy Backtesting Environment

<p align="center">
  <img src="https://github.com/simonpotel/QTSBE/blob/711bb2cecf12bdaef53d9d7a20f05e1971e4af59/files/logo.jpg" width="400" height="400">
</p>

QTSBE is an open-source project aimed at providing a robust environment for backtesting quantitative trading strategies. It includes an API developed in Python using Flask and an interface built with Python.

<p align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Blockchain.com-121D33?logo=blockchaindotcom&logoColor=fff&style=for-the-badge"> 
  <img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white">
</p>

## Features

- Comprehensive backtesting environment for quantitative trading strategies.
- API for strategy implementation and testing.
- Visualization tools for strategy performance.

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
   - Start the GUI for visualizing the API response by running `display/python/main_gui.py`.

   ```bash
   python display/python/main_gui.py
   ```

   - The display tool allows you to select your strategy and the dataset to apply it to.

   Example of the default strategy:

   ![image](https://github.com/simonpotel/QTSBE/assets/155122848/c276e11b-043b-4d45-a58c-a0d776ac9da2)

5. **Real Strategy Stats:**
   - Example of a simple strategy based on Bollinger Bands:

     - Full menu view:

       ![image](https://github.com/simonpotel/QTSBE/blob/711bb2cecf12bdaef53d9d7a20f05e1971e4af59/files/display/python/full_view.png)
       
     - Price Chart:

       ![image](https://github.com/simonpotel/QTSBE/blob/711bb2cecf12bdaef53d9d7a20f05e1971e4af59/files/display/python/price.png)
       
     - Trade Ratio and Cumulative Returns:

       ![image](https://github.com/simonpotel/QTSBE/blob/711bb2cecf12bdaef53d9d7a20f05e1971e4af59/files/display/python/ratio_cumultative.png)
       
     - RSI and MACD Graphs:

       ![image](https://github.com/simonpotel/QTSBE/blob/711bb2cecf12bdaef53d9d7a20f05e1971e4af59/files/display/python/rsi_MACD.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Note: The contents of the files in the indicators folder are not guaranteed to be completely accurate. Always review the code of each indicator before use.

## Requirements

To run this project, you'll need to install the following dependencies:
```bash
pip install -r requirements.txt
```

- [customtkinter](https://pypi.org/project/customtkinter/): A custom themed version of Tkinter, providing enhanced visual elements and features for GUI development.
- [matplotlib](https://pypi.org/project/matplotlib/): A comprehensive library for creating static, animated, and interactive visualizations in Python.
- [loguru](https://pypi.org/project/loguru/): A logging library that provides an easy-to-use interface for logging in Python applications.
- [ccxt](https://pypi.org/project/ccxt/): A cryptocurrency trading library that provides unified APIs for accessing trading data and executing trades across multiple cryptocurrency exchanges.
- [tables](https://pypi.org/project/tables/): A package for managing hierarchical datasets and storing large data arrays efficiently in HDF5 format.
- [plotly](https://pypi.org/project/plotly/): An open-source graphing library for creating interactive, publication-quality graphs and charts.
- [pandas](https://pypi.org/project/pandas/): A powerful data manipulation and analysis library, providing data structures and functions for working with structured data.
- [flask](https://pypi.org/project/Flask/): A lightweight web application framework for Python, providing tools for building web applications and APIs.
- [flask_cors](https://pypi.org/project/Flask-Cors/): A Flask extension for handling Cross-Origin Resource Sharing (CORS), allowing web applications to make requests to domains outside of their own.
- [mysql](https://pypi.org/project/mysql/): A MySQL database connector for Python, enabling interaction with MySQL databases using Python code.
- [mysqlclient](https://pypi.org/project/mysqlclient/): A Python interface to MySQL, providing access to MySQL database servers from Python applications.

## Contact

For questions or inquiries, feel free to contact me on [LinkedIn](https://www.linkedin.com).
