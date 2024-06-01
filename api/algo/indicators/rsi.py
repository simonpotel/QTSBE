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
