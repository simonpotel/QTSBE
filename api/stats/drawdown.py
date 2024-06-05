# Maximum Drawdown: 
# Largest percentage loss from a peak to a trough before a new peak is attained. 
# It helps gauge the worst-case scenario for potential losses.

# Total Drawdown:
# The total drawdown represents the cumulative sum of all individual drawdowns 
# experienced during a series of trades or over a specified period. 
# It offers insight into the overall downside risk inherent in an investment strategy or portfolio.

# Stability Ratio:
# The stability ratio measures the efficiency of returns relative to the worst drawdown experienced. 
# A higher stability ratio indicates better risk-adjusted returns, 
# showing how effectively returns balance against the maximum drawdown.

def get_drawdowns_stats(positions):
    ratios = [trade['ratio'] for trade in positions.positions]

    max_drawdown = 0
    peak = ratios[0]
    start_index = 0
    end_index = 0
    max_drawdown_period = None

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

    total_drawdown = sum([(max(ratios[:i+1]) - ratios[i]) / max(ratios[:i+1]) for i in range(len(ratios))])

    total_return = sum(ratios) - len(ratios)
    stability_ratio = total_return / max_drawdown if max_drawdown != 0 else float('inf')

    return {
        'max_drawdown': max_drawdown,
        'total_drawdown': total_drawdown,
        'stability_ratio': stability_ratio,
        'max_drawdown_period': max_drawdown_period
    }
