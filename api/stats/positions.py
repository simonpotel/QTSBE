from datetime import datetime

def get_position_stats(positions):
    result_stats = {
        'max_loss': 0,
        'max_loss_buy_index': 0,
        'max_loss_sell_index': 0,
        'average_ratio': 1,
        'all_ratios': [0],
        'cumulative_ratios': [0],
        'max_cumulative_ratio': 1,
        'daily_average_ratio': 1,
        'hourly_average_ratio': 1,
        'average_position_duration': 0
    }

    max_loss = float('-inf')
    max_loss_buy_index = None
    max_loss_sell_index = None
    total_ratio = 0
    all_ratios = []
    cumulative_ratios = []
    max_cumulative_ratio = 1  # 1 (we start with no loss)
    total_days = 0
    total_positions = len(positions.positions)
    if total_positions < 1 : return result_stats
    for position in positions.positions:
        loss = position['sell_price'] - position['buy_price']
        if loss > max_loss:
            max_loss = loss
            max_loss_buy_index = position['buy_index']
            max_loss_sell_index = position['sell_index']

        ratio = position['ratio']
        all_ratios.append(ratio)
        total_ratio += ratio

        if not cumulative_ratios:
            cumulative_ratios.append(ratio)
        else:
            cumulative_ratios.append(cumulative_ratios[-1] * ratio)
            if cumulative_ratios[-1] > max_cumulative_ratio:
                max_cumulative_ratio = cumulative_ratios[-1]

        buy_date = datetime.strptime(position['buy_date'], '%Y-%m-%d')
        sell_date = datetime.strptime(position['sell_date'], '%Y-%m-%d')
        duration = sell_date - buy_date
        total_days += duration.days

    average_ratio = total_ratio / total_positions

    daily_average_ratio = average_ratio

    hourly_average_ratio = daily_average_ratio / 24 

    average_position_duration = total_days / total_positions

    result_stats['max_loss'] = max_loss
    result_stats['max_loss_buy_index'] = max_loss_buy_index
    result_stats['max_loss_sell_index'] = max_loss_sell_index
    result_stats['average_ratio'] = average_ratio
    result_stats['all_ratios'] = all_ratios
    result_stats['cumulative_ratios'] = cumulative_ratios
    result_stats['max_cumulative_ratio'] = max_cumulative_ratio
    result_stats['daily_average_ratio'] = daily_average_ratio
    result_stats['hourly_average_ratio'] = hourly_average_ratio
    result_stats['average_position_duration'] = average_position_duration

    return result_stats
