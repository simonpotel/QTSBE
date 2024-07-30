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

    positions.indicators = { 
    }

    return positions
