from datetime import datetime
from stats.trades import Positions

def analyse(data, start_ts, end_ts, multi_positions, strategy, position_type='long'):
    positions = Positions()
    indicators = strategy["Indicators"](data)

    positions.indicators = {key: list(value)
                          for key, value in indicators.indicators.items()}

    for i in range(len(data)):
        data_date = datetime.strptime(data[i][0], "%Y-%m-%d %H:%M:%S")
        if start_ts and data_date < start_ts:
            continue
        if end_ts and data_date > end_ts:
            break

        for position in positions.current_positions[:]:
            sell_signal, sell_price = strategy["sell_signal"](
                position, data, i, indicators.indicators)
            if sell_signal > 0:
                positions.close_position(
                    buy_index=position['buy_index'],
                    sell_index=i,
                    sell_price=sell_price,
                    sell_date=data_date.strftime("%Y-%m-%d %H:%M:%S"),
                    sell_signals={'Sell_Signal': sell_signal}
                )
            position['active_stats'] = {
                "current_ratio": (data[i][4] / position['buy_price']) * (1 - (positions.broker_fees / 100)) if position['position_type'] == 'long' else (position['buy_price'] / data[i][4]) * (1 - (positions.broker_fees / 100)),
                "current_date": data[i][0],
                "current_position_duration": (data_date - datetime.strptime(position['buy_date'], "%Y-%m-%d %H:%M:%S")).days
            }

        if len(positions.current_positions) == 0 or multi_positions:
            buy_signal, buy_price = strategy["buy_signal"](
                positions.current_positions, data, i, indicators.indicators)
            if buy_signal > 0:
                positions.add_position(
                    buy_index=i,
                    buy_price=buy_price,
                    buy_date=data_date.strftime("%Y-%m-%d %H:%M:%S"),
                    buy_signals={'Buy_Signal': buy_signal},
                    position_type=position_type
                )

    return positions 