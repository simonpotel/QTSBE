from datetime import datetime

class Positions(object):
    def __init__(self):
        self.positions = []
        self.current_positions = []
        self.indicators = {}
        self.broker_fees = 0.35 # Default broker fees in %

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
        try:
            buy_date_dt = datetime.strptime(buy_date, "%Y-%m-%d %H:%M:%S")
            sell_date_dt = datetime.strptime(sell_date, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"Error parsing dates: {e}")
            return

        # Calculate position duration correctly
        position_duration = (sell_date_dt - buy_date_dt).days + 1
        self.positions.append(
            {
            'buy_index': buy_index,
            'buy_price': buy_price,
            'buy_date': buy_date_dt.strftime("%Y-%m-%d %H:%M:%S"),
            'buy_signals': buy_signals,
            'sell_index': sell_index,
            'sell_price': sell_price,
            'sell_date': sell_date_dt.strftime("%Y-%m-%d %H:%M:%S"),
            'sell_signals': sell_signals,
            'ratio': ((sell_price / buy_price) * (1-(self.broker_fees/100))),
            'position_duration': position_duration
            }
        )

    def add_position(
            self,
            buy_index,
            buy_price,
            buy_date,
            buy_signals):
        try:
            buy_date_dt = datetime.strptime(buy_date, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"Error parsing buy date: {e}")
            return

        self.current_positions.append({
            'buy_index': buy_index,
            'buy_price': buy_price,
            'buy_date': buy_date_dt.strftime("%Y-%m-%d %H:%M:%S"),
            'buy_signals': buy_signals,
            'active_stats': {
            "current_ratio": 1,
            "current_date": buy_date_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "current_position_duration": 0
            }
        })

    def close_position(
            self,
            buy_index,
            sell_index,
            sell_price,
            sell_date,
            sell_signals):
        try:
            sell_date_dt = datetime.strptime(sell_date, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"Error parsing sell date: {e}")
            return False

        position = next((pos for pos in self.current_positions if pos['buy_index'] == buy_index), None)
        if not position:
            return False

        self.add_trade(
            buy_index=position['buy_index'],
            buy_price=position['buy_price'],
            buy_date=position['buy_date'],
            buy_signals=position['buy_signals'],
            sell_index=sell_index,
            sell_price=sell_price,
            sell_date=sell_date_dt.strftime("%Y-%m-%d %H:%M:%S"),
            sell_signals=sell_signals)
        self.current_positions = [pos for pos in self.current_positions if pos['buy_index'] != buy_index]

if __name__ == "__main__":
    # Example positions on BTC (hypothetical data)
    # To understand how the class works
    positions = Positions()

    # 1st position
    positions.add_position(
        buy_index=1,
        buy_price=50000,
        buy_date="2023-01-01",
        buy_signals=[{'RSI': 30}]
    )
    positions.close_position(
        buy_index=1,
        sell_index=2,
        sell_price=52000,
        sell_date="2023-02-01",
        sell_signals=[{'RSI': 60}]
    )

    # 2nd position
    positions.add_position(
        buy_index=3,
        buy_price=51000,
        buy_date="2023-03-01",
        buy_signals=[{'RSI': 50}]
    )
    positions.close_position(
        buy_index=3,
        sell_index=4,
        sell_price=47000,
        sell_date="2023-04-01",
        sell_signals=[{'RSI': 42}]
    )

    for trade in positions.positions:
        print(trade)
