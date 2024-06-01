class Trades(object):
    def __init__(self):
        self.trades = []
        self.position = {}

    def add_trade(
            self,
            buy_index,
            buy_price,
            buy_date,
            buy_signals,
            sell_index,
            sell_price,
            sell_date,
            sell_signals):
        self.trades.append(
            {
                'buy_index': buy_index,
                'buy_price': buy_price,
                'buy_date': buy_date,
                'buy_signals': buy_signals,
                'sell_index': sell_index,
                'sell_price': sell_price,
                'sell_date': sell_date,
                'sell_signals': sell_signals,
                'ratio': sell_price/buy_price
            }
        )

    def add_position(
            self,
            buy_index,
            buy_price,
            buy_date,
            buy_signals):
        #if self.position != {}: return False 
        self.position = {
                'buy_index': buy_index,
                'buy_price': buy_price,
                'buy_date': buy_date,
                'buy_signals': buy_signals,
        }

    def close_position(
            self,
            sell_index,
            sell_price,
            sell_date,
            sell_signals):
        if self.position == {}: return False 

        self.add_trade(
            buy_index=self.position['buy_index'],
            buy_price=self.position['buy_price'],
            buy_date=self.position['buy_date'],
            buy_signals=self.position['buy_signals'],
            sell_index=sell_index,
            sell_price=sell_price,
            sell_date=sell_date,
            sell_signals=sell_signals)
        self.position = {}

if __name__ == "__main__":
    # Example trades on BTC (hypothetical data)
    # To understand how the class works
    trades = Trades()

    # 1st position
    trades.add_position(
        buy_index=1,
        buy_price=50000,
        buy_date="2023-01-01",
        buy_signals=[{'RSI': 30}]
    )
    trades.close_position(
        sell_index=2,
        sell_price=52000,
        sell_date="2023-02-01",
        sell_signals=[{'RSI': 60}]
    )

    # 2nd position
    trades.add_position(
        buy_index=3,
        buy_price=51000,
        buy_date="2023-03-01",
        buy_signals=[{'RSI': 50}]
    )
    trades.close_position(
        sell_index=4,
        sell_price=47000,
        sell_date="2023-04-01",
        sell_signals=[{'RSI': 42}]
    )

    for trade in trades.trades:
        print(trade)
