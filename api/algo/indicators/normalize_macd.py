import numpy as np

def get_normalize_MACD(macd_line):
    """
    Normalize the MACD line values to be between 0 and 100.

    Parameters:
    macd_line (numpy.ndarray): Array containing the MACD line values.

    Returns:
    numpy.ndarray: An array containing the normalized MACD line values.
    """
    min_macd = np.min(macd_line)
    max_macd = np.max(macd_line)
    normalized_macd = 100 * (macd_line - min_macd) / (max_macd - min_macd)
    return normalized_macd

