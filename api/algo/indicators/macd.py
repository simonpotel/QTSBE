import numpy as np
from algo.indicators.ema import get_EMA

def get_MACD(prices, short_window=12, long_window=26, signal_window=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for a given price series.

    Parameters:
    prices (list or array-like): List or array of price data.
    short_window (int): The window size for the short-term moving average. Default is 12.
    long_window (int): The window size for the long-term moving average. Default is 26.
    signal_window (int): The window size for the signal line. Default is 9.

    Returns:
    (numpy.ndarray, numpy.ndarray): Two arrays containing the MACD line and the signal line.
    """
    short_ema = get_EMA(prices, short_window) # short-term EMA
    long_ema = get_EMA(prices, long_window) # long-term EMA
    macd_line = short_ema - long_ema # MACD line
    signal_line = get_EMA(macd_line, signal_window) # signal line

    return macd_line, signal_line



