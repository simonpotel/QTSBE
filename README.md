
# QTSBE - Quantitative Trading Strategy Backtesting Environment
<center>
<img src="https://github.com/simonpotel/QTSBE/blob/1066ab0d2f039f108cf164dd5cbeb2201705880e/files/logo_nobc.png" width="400" height="400">
QTSBE is an open-source project aimed at providing a robust environment for backtesting quantitative trading strategies. It includes an API developed in Python using Flask and an interface built with Python.

  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"> 

  <img src="https://img.shields.io/badge/Blockchain.com-121D33?logo=blockchaindotcom&logoColor=fff&style=for-the-badge"> 
  
  <img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white"> 
    

## Features

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

1. Create your strategy based on the default structure (api/strategies/default.py) OR copy and past a simple base : api/strategies/rsi_example
2. To create your strategy, you just need to create the file python and create the func analyse thats return the same things has the others strategies. You can choose whether you want to use an indicator in the code but not pass it on in the json response and therefore not display it.
3. You got a simple strategy, now you can start the api in api/api.py
  ![image](https://github.com/simonpotel/QTSBE/assets/155122848/c276e11b-043b-4d45-a58c-a0d776ac9da2)
4. You can get the response of the API on ur web browser (http://127.0.0.1:5000/QTSBE/<data_set>/<your_strategy_name>
5. You can also display the response of the API by starting display/python/main_gui.py
   The display tool will show you this window:
   
   ![image](https://github.com/simonpotel/QTSBE/assets/155122848/e8d91944-8b22-4b24-9c46-1b400a6f0ac1)
   
   And you will be able to select your strategy, and the data thats you want to apply it
   
   ![image](https://github.com/simonpotel/QTSBE/assets/155122848/7dff0f51-fa19-45c7-96dc-3176bc725175)

   If you test with rsi_example, you should get this:

   ![image](https://github.com/simonpotel/QTSBE/blob/74f0a90ba208369710894f12e3734cb6092b8df9/files/rsi_example.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) has been used for API Framework
- NB: The contents of files in indicators are by no means a 100% exact science, and you should always check what you're using.
Check the code of each indicator to be sure of what you're using.

## Contact

For questions or inquiries, feel free to contact me on LinkedIn

</center>
