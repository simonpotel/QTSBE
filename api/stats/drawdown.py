def get_drawdowns_stats(positions):
    result_stats = {
        'max_drawdown': 0,  # largest percentage loss from a peak to a trough
        'max_drawdown_period': 0,  # period during which the maximum drawdown occurred
        'average_drawdown': 0  # average drawdown across all positions
    }

    ratios = [trade['ratio'] for trade in positions.positions]
    if len(ratios) < 1: return result_stats
        
    max_drawdown = 0
    peak = ratios[0]
    start_index = 0
    end_index = 0
    max_drawdown_period = None
    drawdowns = []

    for i, ratio in enumerate(ratios):
        if ratio > peak:
            peak = ratio
        if peak != 0:
            drawdown = (peak - ratio) / peak
        else:
            drawdown = 0
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            start_index = i
            end_index = i
            max_drawdown_period = (positions.positions[start_index]['buy_date'], positions.positions[end_index]['sell_date'])
        elif drawdown == max_drawdown:
            end_index = i
            max_drawdown_period = (positions.positions[start_index]['buy_date'], positions.positions[end_index]['sell_date'])
        drawdowns.append(drawdown)

    average_drawdown = sum(drawdowns) / len(drawdowns)
    result_stats['max_drawdown'] = max_drawdown
    result_stats['max_drawdown_period'] = max_drawdown_period
    result_stats['average_drawdown'] = average_drawdown

    return result_stats
