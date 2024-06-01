from stats.trades import Positions
from api import logger

def analyse(data, prices):
    logger.debug("No analyse (DEFAULT)")
    positions = Positions() # You must create an object of the class positions
    positions.indicators = {
        # This is an example of indicator, but you can use the fonctions in algo/indicators/
        'test': [price*2 for price in prices] 
    }
    return positions

# structure of indicators:
# {
#"mm_20": [] ;tab of values
#}

# structure of trades (2 trades ex)
#      {
#        "buy": {
#          "buy_date": "2021-01-04",
#          "buy_price": 2.1789
#        },
#        "ratio": 1.3719307907659828,
#        "sell": {
#          "sell_date": "2021-01-22",
#          "sell_price": 2.9893
#        }
#      },
#      {
#        "buy": {
#          "buy_date": "2021-01-23",
#          "buy_price": 3.3302
#        },
#        "ratio": 4.251576481892979,
#        "sell": {
#          "sell_date": "2021-03-16",
#          "sell_price": 14.1586
#        }
#      },
#      ...
#      }

# structure of position (number = buy_index = the index where it bought in prices tab)
# ( if there is not any position then its a void dic : {} )
#    {
#      "1362": {
#        "buy_date": "2024-05-04",
#        "buy_price": 143.7
#      }
#    }