import numpy as np


def get_MA(price_tab, window):
    average_tab = [None] * (window - 1)
    for i in range(window - 1, len(price_tab)):
        average = np.mean(price_tab[i - window + 1:i])
        average_tab.append(average)
    return average_tab


def get_bollinger_bands(prices, window=20, num_std_dev=2):
    prices = np.array(prices)
    rolling_mean = np.full_like(prices, np.nan)
    for i in range(window, len(prices)):
        rolling_mean[i] = np.mean(prices[i - window + 1:i + 1])

    rolling_std = np.full_like(prices, np.nan)
    for i in range(window, len(prices)):
        rolling_std[i] = np.std(prices[i - window + 1:i + 1], ddof=1)

    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std

    return upper_band, rolling_mean, lower_band


def get_MACD(prices, slow=26, fast=12, signal=9):
    prices = np.array(prices)
    fast_ema = np.full_like(prices, np.nan)
    slow_ema = np.full_like(prices, np.nan)
    macd = np.full_like(prices, np.nan)
    signal_line = np.full_like(prices, np.nan)

    for i in range(fast, len(prices) + 1):
        fast_ema[i - 1] = np.mean(prices[i - fast:i])
    for i in range(slow, len(prices) + 1):
        slow_ema[i - 1] = np.mean(prices[i - slow:i])

    for i in range(len(prices)):
        if not np.isnan(fast_ema[i]) and not np.isnan(slow_ema[i]):
            macd[i] = fast_ema[i] - slow_ema[i]

    for i in range(signal, len(macd) + 1):
        signal_line[i - 1] = np.mean(macd[i - signal:i])

    return macd, signal_line


def get_ATR(data, window=14):
    high_prices = np.array([row[2] for row in data])
    low_prices = np.array([row[3] for row in data])
    close_prices = np.array([row[4] for row in data])

    tr = np.maximum(high_prices[1:], close_prices[:-1]) - \
        np.minimum(low_prices[1:], close_prices[:-1])
    atr = np.full_like(close_prices, np.nan)

    for i in range(window, len(tr) + 1):
        atr[i] = np.mean(tr[i - window:i])

    return atr


def get_RSI(prices, window=14):
    deltas = np.diff(prices)
    seed = deltas[:window+1]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window

    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100. / (1. + rs)
    for i in range(window, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


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
        raise ValueError(
            "Invalid indices. Ensure start_index is less than end_index.")

    # Find low and high prices from adjusted range
    low_price = min([float(row[3])
                    for row in data[adjusted_start_index:end_index + 1]])
    high_price = max([float(row[2])
                     for row in data[adjusted_start_index:end_index + 1]])
    price_range = high_price - low_price

    retracement_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    retracement_prices = {f"{level * 100:.1f}%": high_price -
                          (price_range * level) for level in retracement_levels}

    return retracement_prices


class Indicators(object):
    def __init__(self, data):
        self.data = data
        self.indicators = {}
        self.indicators['MA_9'] = get_MA([row[4] for row in data], 9)
        self.indicators['MA_21'] = get_MA([row[4] for row in data], 21)
        self.indicators['Bollinger_Upper'], self.indicators['Bollinger_Rolling'], self.indicators['Bollinger_Lower'] = get_bollinger_bands([
                                                                                                                                           row[4] for row in data])
        self.indicators['MACD'], self.indicators['MACD_Signal'] = get_MACD(
            [row[4] for row in data])
        self.indicators['ATR'] = get_ATR(data)
        self.indicators['ATR_MA'] = get_MA(self.indicators['ATR'], 14)
        self.indicators['MA_100'] = get_MA([row[4] for row in data], 100)
        self.indicators['MA_40'] = get_MA([row[4] for row in data], 40)
        self.indicators['MA_200'] = get_MA([row[4] for row in data], 200)
        self.indicators['RSI'] = get_RSI([row[4] for row in data])


def buy_signal(open_position, data, index_check, indicators, current_price=None):
    return 0, None


def sell_signal(open_position, data, index_check, indicators, current_price=None):
    return 0, None
