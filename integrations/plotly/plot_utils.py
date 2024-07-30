import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import webbrowser

chart_colors = {
    "Price": "#6c7386",
    "MA_100": "#B8336A",
    "MA_40": "#FF9B42",
    "MA_20": "#F4D35E",
    "Test": "#C73E1D",
    "RSI": "#9AB87A",
    "EMA": "#F0A7A0",
    "EMA_MACD": "#F0A7A0",
    "MACD": "#5E4AE3",
    "Normalize_MACD": "#947BD3",
    "Bollinger_Lower": "#A682FF",
    "Bollinger_Rolling": "#A682FF",
    "Bollinger_Upper": "#A682FF",
}

def extract_ohlc_data(data):
    """Extract OHLC data from the JSON data."""
    dates, opens, highs, lows, closes, volume = zip(*data)
    return dates, opens, highs, lows, closes

def extract_indicators(json_data):
    """Extract indicators data from the JSON data."""
    indicators = {}
    for indicator in json_data['result'][0]:
        indicators[indicator] = json_data['result'][0][indicator]
    return indicators

def extract_trade_data(trades):
    """Extract trade indices and ratios from the trade data."""
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios

def plot_json_data_in_gui(json_data, data_file, strategy):
    """Plot JSON data in the GUI with candlestick chart, RSI chart (if available), and trade ratios."""
    dates, opens, highs, lows, closes = extract_ohlc_data(json_data['data'])
    indicators = extract_indicators(json_data)
    trades = json_data['result'][1]
    trade_indices, trade_ratios = extract_trade_data(trades)
    rows = 1
    cols = 1

    if 'RSI' or 'Normalize_MACD' in indicators:
        price_row_height = 0.7
        rsi_row_height = 0.3
        rows += 1
    else:
        price_row_height = 1.0
        rsi_row_height = 0.0

    row_heights=[price_row_height]
    if 'RSI' or 'Normalize_MACD' in indicators:
        row_heights.append(rsi_row_height)

    if len(trade_ratios) > 0: cols += 1

    column_widths = [0.7] * cols
    if cols > 1:
        column_widths[0] = 0.7

    fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True, vertical_spacing=0.25,
                        row_heights=row_heights,
                        column_widths=column_widths)

    fig.add_trace(go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes), row=1, col=1)

    for indicator in indicators:
        row = 1
        if indicator == 'RSI' or indicator == 'Normalize_MACD': row += 1
        fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=row, col=1)

    if len(trade_ratios) > 0:
        fig.add_trace(go.Scatter(x=trade_indices, y=trade_ratios, mode='lines', name='Trade Ratios', line=dict(color=chart_colors['Test'])), row=1, col=2)
        cumulative_ratios = [float(cumulative_ratio) for cumulative_ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines', name='Cumulative Ratios', line=dict(color=chart_colors['MA_100'])), row=1, col=2)

    # Add buy/sell markers and hover texts
    # (Include this part of the code similar to the provided code)

    fig.update_layout(title=f"{data_file} ({strategy})",
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False,
                      plot_bgcolor='#161a25',
                      paper_bgcolor='#161a25',
                      font=dict(color='white'),
                      yaxis=dict(gridcolor='#6c7386'),
                      xaxis=dict(gridcolor='#6c7386'),
                      yaxis2=dict(gridcolor='#6c7386'),
                      xaxis2=dict(gridcolor='#6c7386'))

    if 'RSI' or 'Normalize_MACD' in indicators:
        fig.update_yaxes(range=[0, 100], row=2, col=1)
        fig.add_shape(type="line", x0=min(dates), y0=50, x1=max(dates), y1=50, row=2, col=1, line=dict(color="LightSkyBlue", width=3))

    os.makedirs('integrations/plotly/saved_results/', exist_ok=True)
    plot_filename = 'integrations/plotly/saved_results/plot.html'
    fig.write_html(plot_filename)
    webbrowser.open(os.path.join(os.getcwd(), 'integrations', 'plotly', 'saved_results', 'plot.html'))
