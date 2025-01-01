def get_drawdowns_stats(positions):
    result_stats = {
        'max_drawdown': 0,  # largest percentage loss from a peak to a trough
        'max_drawdown_period': 0,  # period during which the maximum drawdown occurred
        'average_drawdown': 0  # average drawdown across all positions
    }

    ratios = [trade['ratio'] for trade in positions.positions]
    if len(ratios) < 1: return result_stats
        
    cumulative_ratios = []
    current_ratio = 1
    for ratio in ratios:
        current_ratio *= ratio
        cumulative_ratios.append(current_ratio)
    
    max_drawdown = 0
    peak_idx = 0
    max_drawdown_start = 0
    max_drawdown_end = 0
    current_peak = cumulative_ratios[0]
    
    for i in range(len(cumulative_ratios)):
        if cumulative_ratios[i] > current_peak:
            current_peak = cumulative_ratios[i]
            peak_idx = i
        else:
            drawdown = (current_peak - cumulative_ratios[i]) / current_peak if current_peak > 0 else 0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_start = peak_idx
                max_drawdown_end = i

    drawdowns = []
    peak = cumulative_ratios[0]
    for ratio in cumulative_ratios:
        if ratio > peak:
            peak = ratio
        drawdown = (peak - ratio) / peak if peak > 0 else 0
        drawdowns.append(drawdown)

    result_stats['max_drawdown'] = max_drawdown
    result_stats['max_drawdown_period'] = (
        positions.positions[max_drawdown_start]['buy_date'],
        positions.positions[max_drawdown_end]['sell_date']
    ) if max_drawdown > 0 else None
    result_stats['average_drawdown'] = sum(drawdowns) / len(drawdowns) if drawdowns else 0

    return result_stats
