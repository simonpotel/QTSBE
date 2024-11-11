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

def get_MA(price_tab, window):
    """
    Calculate the moving average for a given price series.

    Parameters:
    price_tab (list or array-like): List or array of price data.
    window (int): The window size for the moving average calculation.

    Returns:
    list: A list containing the moving averages. Elements before the
          window is filled are set to None.
    """
    average_tab = []
    for i in range(len(price_tab)):
        if i >= window - 1:  # ensure we have enough data points for the window
            # calculate the mean of the current window
            average = np.mean(price_tab[i - window + 1: i + 1])
            # append the moving average to the list
            average_tab.append(average)
        else:
            average_tab.append(None)  # af not enough data points, append None
    return average_tab  # return the list of moving averages


def get_bollinger_bands(prices, window=20, num_std_dev=2):
    """
    Calculate the Bollinger Bands for a given price series.

    Parameters:
    prices (list or array-like): List or array of price data.
    window (int): The window size for the moving average calculation. Default is 20.
    num_std_dev (int): The number of standard deviations for the bands. Default is 2.

    Returns:
    (numpy.ndarray, numpy.ndarray, numpy.ndarray): Three arrays containing the upper band, the middle band (moving average), and the lower band.
    """

    prices = np.array(prices)
    rolling_mean = np.full_like(prices, np.nan)
    for i in range(window, len(prices) + 1):
        rolling_mean[i - 1] = np.mean(prices[i - window:i])

    # rolling standard deviation
    rolling_std = np.full_like(prices, np.nan)
    for i in range(window, len(prices) + 1):
        rolling_std[i - 1] = np.std(prices[i - window:i], ddof=1)

    # upper and lower bands
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std

    return upper_band, rolling_mean, lower_band


def get_fibonacci_retracement_levels(data, start_index, end_index):
    """
    Calculate Fibonacci retracement levels for a given list of prices within specified indices.
    Parameters:
    data (list of float): A list of price values in the format [date, open, high, low, close, volume].
    start_index (int): The start index for the range within the prices list.
    end_index (int): The end index for the range within the prices list.
    Returns:
    dict: A dictionary with Fibonacci retracement levels and their corresponding price values.
    """
    # Adjust start_index to skip the high of the first candle after purchase
    if start_index + 1 <= end_index:
        adjusted_start_index = start_index + 1
    else:
        raise ValueError("Invalid indices. Ensure start_index is less than end_index.")

    # Find low and high prices from adjusted range
    low_price = min([float(row[3]) for row in data[adjusted_start_index:end_index + 1]])
    high_price = max([float(row[2]) for row in data[adjusted_start_index:end_index + 1]])
    price_range = high_price - low_price

    retracement_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    retracement_prices = {f"{level * 100:.1f}%": high_price -
                          (price_range * level) for level in retracement_levels}

    return retracement_prices


class Indicators(object):
    def __init__(self, data):
        self.data = data
        self.indicators = {}
        self.indicators['Bollinger_Upper'], self.indicators['Bollinger_Rolling'], self.indicators['Bollinger_Lower'] = get_bollinger_bands([row[4] for row in data])
        self.indicators['MA_100'] = get_MA([row[4] for row in data], 100)
        self.indicators['MA_20'] = get_MA([row[4] for row in data], 20)
        self.indicators['MA_40'] = get_MA([row[4] for row in data], 40)
        self.indicators['RSI'] = get_RSI([row[4] for row in data])

def buy_signal(open_position, data, index_check, indicators):
    return 0, None


def sell_signal(open_position, data, index_check, indicators):
    return 0, None
