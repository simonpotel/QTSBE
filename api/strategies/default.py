from algo.indicators.ma import get_MA
from algo.indicators.rsi import get_RSI
from algo.indicators.macd import get_MACD
from algo.indicators.ema import get_EMA
from algo.indicators.normalize_macd import get_normalize_MACD
from algo.indicators.bollinger_bands import get_bollinger_bands
from stats.trades import Positions
from api import logger

def analyse(data, prices, start_ts, end_ts, multi_positions):
    positions = Positions()

    # indicators used in this strategy
    ma_20            = get_MA(prices, 20)
    ma_40            = get_MA(prices, 40)
    ma_100           = get_MA(prices, 100)
    rsi              = get_RSI(prices, 14)
    macd, ema_macd   = get_MACD(prices)
    normalize_macd   = get_normalize_MACD(macd)
    bollinger_upper, bollinger_rolling, bollinger_lower = get_bollinger_bands(prices)

    positions.indicators = {  # must convert all to a list because its using np (Object of type ndarray is not JSON serializable)
        "MA_20": list(ma_20),
        "MA_40": list(ma_40),
        "MA_100": list(ma_100),
        "RSI": list(rsi),
        "MACD": list(macd),
        "EMA_MACD": list(ema_macd),
        "Normalize_MACD": list(normalize_macd),
        "Bollinger_Lower": list(bollinger_lower),
        "Bollinger_Rolling": list(bollinger_rolling),
        "Bollinger_Upper": list(bollinger_upper),
    }

    #for i in range(len(prices) - 1):  # iterate through each price entry
        #if indicator[i] is None: continue  # no data on a indicator (for the first data of prices)

        #if positions.current_position == {}: # not already in a position
            #
        #else:
            #

    return positions
