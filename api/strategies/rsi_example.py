import numpy as np

# Article to understand the RSI : https://admiralmarkets.com/fr/formation/articles/indicateurs-forex/indicateur-rsi

def get_RSI(prices, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given price series.

    Parameters:
    prices (list or array-like): List or array of price data.
    window (int): The window size for the RSI calculation. Default is 14.

    Returns:
    numpy.ndarray: An array containing the RSI values for the given price series. (NB: You must convert it to use it in a Python List)
    """
    
    deltas = np.diff(prices) # tab of price differences between consecutive days
    seed = deltas[:window+1]
    
    # caverage gain and loss over the window period
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    
    rs = up / down # calculate the initial Relative Strength (RS)
    rsi = np.zeros_like(prices) # create the RSI array with zeros, the same length as prices
    rsi[:window] = 100. - 100. / (1. + rs) # set the first window RSI values using the initial RS calculation
    for i in range(window, len(prices)): # calculate RSI for the rest of the prices using a iterrative while
        delta = deltas[i - 1]  # get the price change for the current period
        # determine the gain (upval) and loss (downval) for the current period
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        # update the average gain and loss with the current values
        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


# This example of analysis shows you 
# how you can use an indicator along with classes and functions of QTSBE
# to create your own strategy.

# ⚠️⚠️⚠️ Note that this is an example that does not actually work in the market, 
# as it is based only on a single indicator and a price check that I implemented for selling to avoid losing money. 
# This is why, if you run this example on BTCUSDT since 2018, 
# you will only have 20 transactions and only a 3x increase in your capital over 6 years. 

class Indicators(object):
    def __init__(self, data):
        self.data = data
        self.indicators = self.calculate_indicators()

    def calculate_indicators(self):
        data_open = [row[1] for row in self.data]

        indicators = {
            "RSI": get_RSI(data_open),
        }
        return {k: list(v) for k, v in indicators.items()}


def buy_signal(open_position, data, index_check, indicators):
    if indicators["RSI"][index_check] is None:
        return -2, None
    if indicators["RSI"][index_check] < 40:
        return 1, data[index_check][4]
    return 0, None


def sell_signal(open_position, data, index_check, indicators):
    if indicators["RSI"][index_check] is None:
        return -1, None
    if open_position.get('buy_signal') == 1 or open_position.get('buy_signals', {}).get('Buy_Signal') == 1:
        if open_position['buy_index'] < index_check < len(data):
            if indicators["RSI"][index_check] > 50 and data[index_check][2] / open_position['buy_price'] > 1.10:
                return 1, data[index_check][4]
    return 0, None
