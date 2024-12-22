from datetime import datetime, timedelta
from collections import defaultdict

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
        'sell_signals_count': {},
        'yearly_ratio': {}, 
        'max_open_positions_period': ('', '', 0),  # ('start_date', 'end_date', max_open_positions)
        'biggest_position_duration': 0,
        'lowest_position_duration': float('inf'),
        'lowest_cr_ratio': float('inf'),
        'lowest_cr_ratio_details': []  # Add this line to store the details
    }

    if not positions.positions:
        return result_stats

    total_ratio = 0
    cumulative_ratios = []
    total_days = 0
    open_positions = defaultdict(int)

    for position in positions.positions:
        ratio = position['ratio']
        buy_index, sell_index = position['buy_index'], position['sell_index']
        buy_date = datetime.strptime(position['buy_date'], '%Y-%m-%d %H:%M:%S')
        sell_date = datetime.strptime(position['sell_date'], '%Y-%m-%d %H:%M:%S')
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

        if duration < result_stats['lowest_position_duration']:
            result_stats['lowest_position_duration'] = duration
        if duration > result_stats['biggest_position_duration']:
            result_stats['biggest_position_duration'] = duration

        result_stats['buy_signals_count'][buy_signal] = result_stats['buy_signals_count'].get(buy_signal, 0) + 1
        result_stats['sell_signals_count'][sell_signal] = result_stats['sell_signals_count'].get(sell_signal, 0) + 1

        sell_year = sell_date.year
        if sell_year not in result_stats['yearly_ratio']:
            result_stats['yearly_ratio'][sell_year] = 1
        result_stats['yearly_ratio'][sell_year] *= ratio

        # Track open positions
        current_date = buy_date
        while current_date <= sell_date:
            open_positions[current_date] += 1
            current_date += timedelta(days=1)

    max_open_positions = 0
    max_open_period_start = None
    max_open_period_end = None
    current_max_open = 0
    current_start = None

    for date in sorted(open_positions):
        if open_positions[date] > current_max_open:
            current_max_open = open_positions[date]
            current_start = date
        elif open_positions[date] < current_max_open:
            if current_max_open > max_open_positions:
                max_open_positions = current_max_open
                max_open_period_start = current_start
                max_open_period_end = date - timedelta(days=1)
            current_max_open = open_positions[date]
            current_start = date

    if current_max_open > max_open_positions:
        max_open_positions = current_max_open
        max_open_period_start = current_start
        max_open_period_end = date

    for year in result_stats['yearly_ratio']:
        result_stats['yearly_ratio'][year] = round(result_stats['yearly_ratio'][year], 3)

    min_cr_ratio = float('inf')
    current_cr_ratio = 1
    cr_ratio_details = []  # Add this line to store the details
    for ratio in result_stats['all_ratios']:
        current_cr_ratio *= ratio
        cr_ratio_details.append(current_cr_ratio)  # Add this line to store the details
        if current_cr_ratio < min_cr_ratio:
            min_cr_ratio = current_cr_ratio
        if current_cr_ratio > 1:
            current_cr_ratio = 1

    result_stats.update({
        'average_ratio': total_ratio / len(positions.positions),
        'cumulative_ratios': cumulative_ratios,
        'min_cumulative_ratio': min(cumulative_ratios),
        'max_cumulative_ratio': max(cumulative_ratios),
        'final_cumulative_ratio': cumulative_ratios[-1],
        'average_cumulative_ratio': sum(cumulative_ratios) / len(cumulative_ratios),
        'average_position_duration': total_days / len(positions.positions),
        'max_open_positions_period': (max_open_period_start.strftime('%Y-%m-%d %H:%M:%S') if max_open_period_start else '',
                                      max_open_period_end.strftime('%Y-%m-%d %H:%M:%S') if max_open_period_end else '',
                                      max_open_positions),
        'lowest_cr_ratio': min_cr_ratio,
        'lowest_cr_ratio_details': cr_ratio_details  # Add this line to include the details in the result
    })

    return result_stats
