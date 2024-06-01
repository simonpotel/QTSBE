from stats.trades import Positions
from api import logger

def analyse(data, prices):
    positions = Positions()

    positions.indicators = {  # must convert all to a list because its using np (Object of type ndarray is not JSON serializable)
    }

    #for i in range(len(prices) - 1):  # iterate through each price entry
        #if indicator[i] is None: continue  # no data on a indicator (for the first data of prices)

        #if positions.current_position == {}: # not already in a position
            #
        #else:
            #

    return positions
