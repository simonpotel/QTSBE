import numpy as np

def get_EMA(prices, window):
    """
    Calculate the Exponential Moving Average (EMA) for a given price series.

    Parameters:
    prices (list or array-like): List or array of price data.
    window (int): The window size for the EMA calculation.

    Returns:
    numpy.ndarray: An array containing the EMA values for the given price series.
    """
    ema = np.zeros_like(prices)  # create an array to store the EMA values
    ema[window-1] = np.mean(prices[:window])  # calculate the initial EMA value
    multiplier = 2 / (window + 1)  # calculate the EMA multiplier

    # calculate EMA for the rest of the values
    for i in range(window, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]

    return ema
