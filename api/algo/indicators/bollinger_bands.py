import numpy as np

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
    residuals = prices - rolling_mean

    # rolling standard deviation
    rolling_std = np.full_like(prices, np.nan)
    for i in range(window, len(prices) + 1):
        rolling_std[i - 1] = np.std(prices[i - window:i], ddof=1)

    # upper and lower bands
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std

    return upper_band, rolling_mean, lower_band
