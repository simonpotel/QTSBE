import numpy as np

# Good article to understand the cross between 2 Moving Averrage windows (example 40 and 100)
# https://www.investopedia.com/terms/m/movingaverage.asp

def get_MM(price_tab, window):
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
            average = np.mean(price_tab[i - window + 1 : i + 1])  # calculate the mean of the current window
            average_tab.append(average)  # append the moving average to the list
        else:
            average_tab.append(None)  # af not enough data points, append None
    return average_tab  # return the list of moving averages
