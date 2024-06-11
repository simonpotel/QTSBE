from datetime import datetime

def get_position_stats(positions):
    result_stats = {
        'lowest_ratio': float('inf'),
        'lowest_ratio_buy_index': 0,
        'lowest_ratio_sell_index': 0,
        'biggest_ratio': float('-inf'),
        'biggest_ratio_buy_index': 0,
        'biggest_ratio_sell_index': 0,
        'average_ratio': 1,
        'all_ratios': [],
        'cumulative_ratios': [],
        'max_cumulative_ratio': 1,
        'average_position_duration': 0,
        'buy_signals_count': {},
        'sell_signals_count': {}
    }

    lowest_ratio = float('inf')
    lowest_ratio_buy_index = None
    lowest_ratio_sell_index = None
    biggest_ratio = float('-inf')
    biggest_ratio_buy_index = None
    biggest_ratio_sell_index = None
    total_ratio = 0
    all_ratios = []
    cumulative_ratios = []
    max_cumulative_ratio = 1  # 1 (we start with no loss)
    total_days = 0
    total_positions = len(positions.positions)
    if total_positions < 1:
        return result_stats

    for position in positions.positions:
        ratio = position['ratio']
        all_ratios.append(ratio)
        total_ratio += ratio

        if ratio < lowest_ratio:
            lowest_ratio = ratio
            lowest_ratio_buy_index = position['buy_index']
            lowest_ratio_sell_index = position['sell_index']

        if ratio > biggest_ratio:
            biggest_ratio = ratio
            biggest_ratio_buy_index = position['buy_index']
            biggest_ratio_sell_index = position['sell_index']

        if not cumulative_ratios:
            cumulative_ratios.append(ratio)
        else:
            cumulative_ratios.append(cumulative_ratios[-1] * ratio)
        max_cumulative_ratio = cumulative_ratios[-1]

        buy_date = datetime.strptime(position['buy_date'], '%Y-%m-%d')
        sell_date = datetime.strptime(position['sell_date'], '%Y-%m-%d')
        duration = sell_date - buy_date
        total_days += duration.days
        
        if position['buy_signals']["Buy_Signal"] not in result_stats['buy_signals_count']:
            result_stats['buy_signals_count'][position['buy_signals']["Buy_Signal"]] = 1
        else:
            result_stats['buy_signals_count'][position['buy_signals']["Buy_Signal"]] += 1

        if position['sell_signals']["Sell_Signal"] not in result_stats['sell_signals_count']:
            result_stats['sell_signals_count'][position['sell_signals']["Sell_Signal"]] = 1
        else:
            result_stats['sell_signals_count'][position['sell_signals']["Sell_Signal"]] += 1


    average_ratio = total_ratio / total_positions
    average_position_duration = total_days / total_positions

    result_stats['lowest_ratio'] = lowest_ratio
    result_stats['lowest_ratio_buy_index'] = lowest_ratio_buy_index
    result_stats['lowest_ratio_sell_index'] = lowest_ratio_sell_index
    result_stats['biggest_ratio'] = biggest_ratio
    result_stats['biggest_ratio_buy_index'] = biggest_ratio_buy_index
    result_stats['biggest_ratio_sell_index'] = biggest_ratio_sell_index
    result_stats['average_ratio'] = average_ratio
    result_stats['all_ratios'] = all_ratios
    result_stats['cumulative_ratios'] = cumulative_ratios
    result_stats['max_cumulative_ratio'] = max_cumulative_ratio
    result_stats['average_position_duration'] = average_position_duration

    return result_stats