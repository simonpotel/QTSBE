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

    # Calculate the initial EMA value with a dynamic window size
    initial_window = min(window, len(prices))
    if initial_window == 0:
        return ema  # Return zeros array if there are no prices
    ema[initial_window-1] = np.mean(prices[:initial_window])

    multiplier = 2 / (initial_window + 1)  # calculate the EMA multiplier

    # calculate EMA for the rest of the values
    for i in range(initial_window, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]

    return ema