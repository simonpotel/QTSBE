def get_position_stats(positions):
    max_loss = float('-inf')
    max_loss_buy_index = None
    max_loss_sell_index = None
    total_ratio = 0
    total_profit_ratio = 0
    all_ratios = []
    cumulative_ratios = []
    max_cumulative_ratio = 1 # 1 (we start with no loss)
    for position in positions.positions:
        loss = position['sell_price'] - position['buy_price']
        if loss > max_loss:
            max_loss = loss
            max_loss_buy_index = position['buy_index']
            max_loss_sell_index = position['sell_index']

        ratio = position['ratio']
        all_ratios.append(ratio)
        total_ratio += ratio

        if ratio > 1:
            total_profit_ratio += ratio - 1

        if not cumulative_ratios:
            cumulative_ratios.append(ratio)
        else:
            cumulative_ratios.append(cumulative_ratios[-1] * ratio)
            if cumulative_ratios[-1] > max_cumulative_ratio:
                max_cumulative_ratio = cumulative_ratios[-1]

    average_ratio = total_ratio / len(positions.positions)
    average_annual_profit_ratio = total_profit_ratio / len(positions.positions)

    return {
        'max_loss': max_loss,
        'max_loss_buy_index': max_loss_buy_index,
        'max_loss_sell_index': max_loss_sell_index,
        'average_ratio': average_ratio,
        'average_annual_profit_ratio': average_annual_profit_ratio,
        'all_ratios': all_ratios,
        'cumulative_ratios': cumulative_ratios,
        'max_cumulative_ratio': max_cumulative_ratio
    }
