import math
from datetime import datetime
from statistics import mean, stdev
from typing import List

def _parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def _returns_from_ratios(ratios: List[float]) -> List[float]:
    return [r - 1 for r in ratios]

def get_advanced_stats(positions_obj):
    stats = {
        'sharpe_ratio': None,
        'sortino_ratio': None,
        'volatility': None,
        'max_drawdown_period_days': None,
        'recovery_factor': None,
        'calmar_ratio': None,
        'win_rate': None,
        'loss_rate': None,
        'profit_factor': None,
        'expectancy': None,
        'trade_frequency_per_year': None,
        'exposure_pct': None,
        'annualized_return': None,
        'skewness': None,
        'kurtosis': None,
        'VaR_95': None,
        'CVaR_95': None,
        'consecutive_wins': None,
        'consecutive_losses': None,
        'time_to_recovery_days': None,
    }

    trades = positions_obj.positions
    if not trades:
        return stats

    ratios = [t['ratio'] for t in trades]
    returns = _returns_from_ratios(ratios)

    avg_ret = mean(returns)
    vol = stdev(returns) if len(returns) > 1 else 0
    stats['volatility'] = vol

    if vol != 0:
        stats['sharpe_ratio'] = (avg_ret / vol) * math.sqrt(len(returns))

    downside_returns = [r for r in returns if r < 0]
    if downside_returns:
        downside_std = stdev(downside_returns) if len(downside_returns) > 1 else 0
        if downside_std != 0:
            stats['sortino_ratio'] = (avg_ret / downside_std) * math.sqrt(len(returns))

    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r <= 0]

    stats['win_rate'] = len(wins) / len(returns)
    stats['loss_rate'] = len(losses) / len(returns)

    gross_profit = sum(wins)
    gross_loss = abs(sum(losses)) if losses else 0
    stats['profit_factor'] = gross_profit / gross_loss if gross_loss != 0 else None

    stats['expectancy'] = avg_ret

    buy_dates = [_parse_date(t['buy_date']) for t in trades]
    sell_dates = [_parse_date(t['sell_date']) for t in trades]
    period_days = (max(sell_dates) - min(buy_dates)).days + 1
    stats['trade_frequency_per_year'] = len(trades) / (period_days / 365) if period_days > 0 else None

    total_position_days = sum(t['position_duration'] for t in trades)
    stats['exposure_pct'] = total_position_days / period_days if period_days > 0 else None

    final_cum = 1
    for r in ratios:
        final_cum *= r
    years = period_days / 365
    if years > 0:
        stats['annualized_return'] = final_cum ** (1 / years) - 1

    if vol != 0:
        n = len(returns)
        m3 = sum((r - avg_ret) ** 3 for r in returns) / n
        m4 = sum((r - avg_ret) ** 4 for r in returns) / n
        stats['skewness'] = m3 / (vol ** 3)
        stats['kurtosis'] = m4 / (vol ** 4)

    sorted_returns = sorted(returns)
    var_index = int(0.05 * len(sorted_returns))
    if len(sorted_returns) > 0:
        var_95 = sorted_returns[var_index]
        stats['VaR_95'] = var_95
        stats['CVaR_95'] = mean(sorted_returns[:var_index + 1])

    max_consec_win = max_consec_loss = 0
    current_win = current_loss = 0
    for r in returns:
        if r > 0:
            current_win += 1
            current_loss = 0
        else:
            current_loss += 1
            current_win = 0
        max_consec_win = max(max_consec_win, current_win)
        max_consec_loss = max(max_consec_loss, current_loss)
    stats['consecutive_wins'] = max_consec_win
    stats['consecutive_losses'] = max_consec_loss

    cumulative = []
    c = 1
    for r in ratios:
        c *= r
        cumulative.append(c)

    peak = cumulative[0]
    trough_index = peak_index = 0
    max_drawdown = 0
    recovery_days = None
    for i, val in enumerate(cumulative):
        if val > peak:
            peak = val
            peak_index = i
        drawdown = (peak - val) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            trough_index = i
    if max_drawdown > 0:
        for j in range(trough_index, len(cumulative)):
            if cumulative[j] >= peak:
                recovery_days = (_parse_date(trades[j]['sell_date']) - _parse_date(trades[trough_index]['sell_date'])).days
                break
    stats['time_to_recovery_days'] = recovery_days
    stats['max_drawdown_period_days'] = (_parse_date(trades[trough_index]['sell_date']) - _parse_date(trades[peak_index]['sell_date'])).days if max_drawdown > 0 else None
    stats['recovery_factor'] = final_cum / max_drawdown if max_drawdown > 0 else None
    stats['calmar_ratio'] = stats['annualized_return'] / max_drawdown if max_drawdown > 0 else None

    return stats 