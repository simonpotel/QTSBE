def get_drawdowns_stats(positions):
    ratios = [trade['ratio'] for trade in positions.positions]

    if not ratios:
        return {
            'max_drawdown': 0,
            'total_drawdown': 0,
            'stability_ratio': 0,
            'max_drawdown_period': [0, 0],
            'average_drawdown': 0
        }

    max_drawdown = 0
    peak = ratios[0]
    start_index = 0
    end_index = 0
    max_drawdown_period = None
    drawdowns = []

    for i, ratio in enumerate(ratios):
        if ratio > peak:
            peak = ratio
        drawdown = (peak - ratio) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            start_index = i
            end_index = i
            max_drawdown_period = (positions.positions[start_index]['buy_date'], positions.positions[end_index]['sell_date'])
        elif drawdown == max_drawdown:
            end_index = i
            max_drawdown_period = (positions.positions[start_index]['buy_date'], positions.positions[end_index]['sell_date'])
        drawdowns.append(drawdown)

    total_drawdown = sum([(max(ratios[:i+1]) - ratios[i]) / max(ratios[:i+1]) for i in range(len(ratios))])

    total_return = sum(ratios) - len(ratios)
    stability_ratio = total_return / max_drawdown if max_drawdown != 0 else float('inf')

    average_drawdown = sum(drawdowns) / len(drawdowns)

    return {
        'max_drawdown': max_drawdown,  # cargest percentage loss from a peak to a trough
        'total_drawdown': total_drawdown,  # cumulative sum of all individual drawdowns
        'stability_ratio': stability_ratio,  # efficiency of returns relative to the worst drawdown
        'max_drawdown_period': max_drawdown_period,  # period during which the maximum drawdown occurred
        'average_drawdown': average_drawdown  # average drawdown across all positions
    }

