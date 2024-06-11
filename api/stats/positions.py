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

    if not positions.positions:
        return result_stats

    total_ratio = 0
    cumulative_ratios = []
    total_days = 0

    for position in positions.positions:
        ratio = position['ratio']
        buy_index, sell_index = position['buy_index'], position['sell_index']
        buy_date = datetime.strptime(position['buy_date'], '%Y-%m-%d')
        sell_date = datetime.strptime(position['sell_date'], '%Y-%m-%d')
        duration = (sell_date - buy_date).days
        buy_signal = position['buy_signals']["Buy_Signal"]
        sell_signal = position['sell_signals']["Sell_Signal"]

        total_ratio += ratio
        result_stats['all_ratios'].append(ratio)
        cumulative_ratios.append(cumulative_ratios[-1] * ratio if cumulative_ratios else ratio)
        total_days += duration
        
        if ratio < result_stats['lowest_ratio']:
            result_stats['lowest_ratio'], result_stats['lowest_ratio_buy_index'], result_stats['lowest_ratio_sell_index'] = ratio, buy_index, sell_index
        if ratio > result_stats['biggest_ratio']:
            result_stats['biggest_ratio'], result_stats['biggest_ratio_buy_index'], result_stats['biggest_ratio_sell_index'] = ratio, buy_index, sell_index

        result_stats['buy_signals_count'][buy_signal] = result_stats['buy_signals_count'].get(buy_signal, 0) + 1
        result_stats['sell_signals_count'][sell_signal] = result_stats['sell_signals_count'].get(sell_signal, 0) + 1

    result_stats.update({
        'average_ratio': total_ratio / len(positions.positions),
        'cumulative_ratios': cumulative_ratios,
        'max_cumulative_ratio': cumulative_ratios[-1],
        'average_position_duration': total_days / len(positions.positions)
    })

    return result_stats
