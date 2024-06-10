import numpy as np
import matplotlib.pyplot as plt

def get_fibonacci_retracement_levels(prices, low_index, high_index):
    """
    Calculate the Fibonacci retracement levels for a given price series.

    Parameters:
    prices (list or array-like): List or array of price data.

    Returns:
    dict: A dictionary containing the Fibonacci retracement levels.
    """
    
    prices = np.array(prices)
    high_price = prices[high_index]
    low_price = prices[low_index]
    
    diff = high_price - low_price
    
    levels = {
        '0%': high_price,
        '23.6%': high_price - 0.236 * diff,
        '38.2%': high_price - 0.382 * diff,
        '50%': high_price - 0.5 * diff,
        '61.8%': high_price - 0.618 * diff,
        '100%': low_price
    }
    
    return levels


