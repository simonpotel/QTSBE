import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
#import webbrowser
#from datetime import datetime 

theme = 'white' # black / white

chart_colors = {
    "Background": "white" if theme == 'white' else "black", # black
    "increasing_line": "#1e90ff",
    "increasing_fill": "#115290",
    "decreasing_line": "#d17123",  #red: #be0000  | #orange: #d17123  | 
    "decreasing_fill": "#eb7f26",  #red: #ff0000  | #orange: #eb7f26  | 
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

    fig.add_trace(go.Candlestick(
        x=dates, open=opens, high=highs, low=lows, close=closes,
        name="Price", 
        increasing_line_color=chart_colors['increasing_line'], decreasing_line_color=chart_colors['decreasing_line'], 
        increasing_fillcolor=chart_colors['increasing_fill'], decreasing_fillcolor=chart_colors['decreasing_fill']
    ), row=1, col=1)

    for indicator in indicators:
        row = 1
        if indicator == 'RSI' or indicator == 'Normalize_MACD': row += 1
        fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=row, col=1)

    if len(trade_ratios) > 0:
        fig.add_trace(go.Scatter(x=trade_indices, y=trade_ratios, mode='lines', name='Trade Ratios', line=dict(color=chart_colors['Test'])), row=1, col=2)
        cumulative_ratios = [float(cumulative_ratio) for cumulative_ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines', name='Cumulative Ratios', line=dict(color=chart_colors['MA_100'])), row=1, col=2)

    buy_dates = [trade['buy_date'] for trade in trades]
    buy_prices = [trade['buy_price'] for trade in trades]
    buy_indices = [trade['buy_index'] for trade in trades]  
    buy_signals = [trade['buy_signals']['Buy_Signal'] for trade in trades] 

    sell_dates = [trade['sell_date'] for trade in trades]
    sell_prices = [trade['sell_price'] for trade in trades]
    sell_indices = [trade['sell_index'] for trade in trades]  
    sell_signals = [trade['sell_signals']['Sell_Signal'] for trade in trades] 

    ratios = [float(ratio) for ratio in json_data["stats"]["positions"]["all_ratios"]]

    # hover texts for the markets
    buy_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Buy Signal: {buy_signal}" for index, price, date, buy_signal in zip(buy_indices, buy_prices, buy_dates, buy_signals)]
    sell_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Ratio: {ratio}<br>Sell Signal: {sell_signal}" for index, price, date, ratio, sell_signal in zip(sell_indices, sell_prices, sell_dates, ratios, sell_signals)]

    # plot buy/sell markes
    fig.add_trace(go.Scatter(
        x=buy_dates, 
        y=buy_prices, 
        mode='markers', 
        name='Buy', 
        marker=dict(symbol='triangle-up', color='#B0FE76', size=10),
        hovertext=buy_hover_texts,  
        hoverinfo='text'  
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=sell_dates, 
        y=sell_prices, 
        mode='markers', 
        name='Sell', 
        marker=dict(symbol='triangle-down', color='#2DC7FF', size=10),
        hovertext=sell_hover_texts,  
        hoverinfo='text' 
    ), row=1, col=1)

    fig.update_layout(title=f"{data_file} ({strategy})",
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False,
                      plot_bgcolor=chart_colors['Background'],
                      paper_bgcolor=chart_colors['Background'],
                      font=dict(color="black" if theme == 'white' else "white"),
                      yaxis=dict(gridcolor=chart_colors['Background']),
                      xaxis=dict(gridcolor=chart_colors['Background']),
                      yaxis2=dict(gridcolor=chart_colors['Background']),
                      xaxis2=dict(gridcolor=chart_colors['Background']))

    if 'RSI' or 'Normalize_MACD' in indicators:
        fig.update_yaxes(range=[0, 100], row=2, col=1)
        fig.add_shape(type="line", x0=min(dates), y0=50, x1=max(dates), y1=50, row=2, col=1, line=dict(color="LightSkyBlue", width=3))

    fig.show()

    directory = 'integrations/plotly/saved_results/'
    os.makedirs(directory, exist_ok=True)
    plot_filename = f'plot_{data_file}_{strategy}.html'
    fig.write_html(directory + plot_filename)
    #webbrowser.open(os.path.join(os.getcwd(), 'integrations', 'plotly', 'saved_results', plot_filename)) # save html file
