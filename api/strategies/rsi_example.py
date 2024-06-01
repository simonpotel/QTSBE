from algo.indicators.mm import get_MM
from algo.indicators.rsi import get_rsi
from stats.trades import Trades

# This example of analysis shows you 
# how you can use an indicator along with classes and functions of QTSBE
# to create your own strategy.

# ⚠️⚠️⚠️ Note that this is an example that does not actually work in the market, 
# as it is based only on a single indicator and a price check that I implemented for selling to avoid losing money. 
# This is why, if you run this example on BTCUSDT since 2018, 
# you will only have 20 transactions and only a 3x increase in your capital over 6 years. 

def analyse(data, prices):
    trades = Trades()  

    # indicators used in this strategy example
    rsi = get_rsi(prices, 14)
    indicators = {  # must convert all to a list because its using np (Object of type ndarray is not JSON serializable)
        "rsi": list(rsi)
    }

    for i in range(len(prices) - 1):  # iterate through each price entry
        if rsi[i] is None: continue  # no data on RSI (for the first data of prices)

        if trades.position == {}: # not already in a position
            if rsi[i] < 40:  # RSI is less than 40, buy signal
                trades.add_position(
                    buy_index=i,
                    buy_price=prices[i],
                    buy_date=data[i][0],
                    buy_signals={
                        "rsi": rsi[i]
                    }
                )
        else:
            if rsi[i] > 50 and prices[i]/trades.position['buy_price'] > 1.01:  # RSI > 55 and simple check ratio (⚠️ Dont do this)
                trades.close_position(
                    sell_index=i,
                    sell_price=prices[i],
                    sell_date=data[i][0],
                    sell_signals={
                        "rsi": rsi[i]
                    }
                )

    return indicators, trades.trades, trades.position

