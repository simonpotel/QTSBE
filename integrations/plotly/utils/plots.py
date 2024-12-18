import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os

theme = 'white' # black / white

chart_colors = {
    "Background": theme, # black
    "increasing_line": "black", #blue: #1e90ff  | #green: #00ff00  |
    "increasing_fill": "white", #blue: #115290  | #green: #00b300  |
    "decreasing_line": "black",  #red: #be0000  | #orange: #d17123  | 
    "decreasing_fill": "black",  #red: #ff0000  | #orange: #eb7f26  | 
    "shapes": "#8288b0",
    "MA_100": "#B8336A",
    "MA_40": "#FF9B42",
    "MA_20": "#F4D35E", 
    "Test": "#C73E1D",
    "RSI": "#9AB87A",
    "EMA": "#F0A7A0",
    "EMA_MACD": "#F0A7A0",
    "MACD": "#5E4AE3",
    "Normalize_MACD": "#947BD3",
    "Bollinger_Lower": "#09917b",
    "Bollinger_Rolling": "#2652cb",
    "Bollinger_Upper": "#c9313f",
    "Else": "#8FF7A7",
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
    
    # Determine the number of rows and columns based on indicators and trade ratios
    rows = 2
    cols = 1
    bound_hundred_plot = True if 'RSI' in indicators or 'Normalize_MACD' in indicators else False 

    if bound_hundred_plot and len(trade_ratios) > 0:
        cols += 1
    if not bound_hundred_plot and len(trade_ratios) == 0: rows = 1

    if cols == 1 and rows == 2:
        row_heights = [0.7, 0.3]
        column_widths = [1]
    elif cols == 2 and rows == 2:
        row_heights = [0.75, 0.25]
        column_widths = [0.75, 0.25]
    elif rows == 1:
        row_heights = [1]
        column_widths = [1]

    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes='all',
        vertical_spacing=0.25,
        row_heights=row_heights,
        column_widths=column_widths
    )

    # Add candlestick chart to the first row, first column
    fig.add_trace(go.Candlestick(
        x=dates, open=opens, high=highs, low=lows, close=closes,
        name="Price", 
        increasing_line_color=chart_colors['increasing_line'], decreasing_line_color=chart_colors['decreasing_line'], 
        increasing_fillcolor=chart_colors['increasing_fill'], decreasing_fillcolor=chart_colors['decreasing_fill']
    ), row=1, col=1)


    # Add trade ratios chart to the second column if there are trade ratios
    if len(trade_ratios) > 0:
        fig.add_trace(go.Scatter(x=trade_indices, y=trade_ratios, mode='lines', name='Trade Ratios', line=dict(color='#DBB4AD')), row=1 if bound_hundred_plot else 2, col=2 if bound_hundred_plot else 1)
        cumulative_ratios = [float(cumulative_ratio) for cumulative_ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines', name='Cumulative Ratios', line=dict(color='#D30C7B')), row=1 if bound_hundred_plot else 2, col=2 if bound_hundred_plot else 1)
        fig.add_shape(type="line", x0=min(trade_indices), y0=1, x1=max(trade_indices), y1=1, row=1 if bound_hundred_plot else 2, col=2 if bound_hundred_plot else 1, line=dict(color=chart_colors['shapes'], width=1.5))

        min_ratio = min(trade_ratios)
        fig.add_shape(type="line", x0=min(trade_indices), y0=min_ratio, x1=max(trade_indices), y1=min_ratio, row=1 if bound_hundred_plot else 2, col=2 if bound_hundred_plot else 1, line=dict(color='red', width=1.5, dash='dash'))

        moving_avg_cumulative_ratios = [sum(cumulative_ratios[:i+1])/(i+1) for i in range(len(cumulative_ratios))]
        fig.add_trace(go.Scatter(x=trade_indices, y=moving_avg_cumulative_ratios, mode='lines', name='Moving Avg Cumulative Ratios', line=dict(color='#FFE3DC')), row=1 if bound_hundred_plot else 2, col=2 if bound_hundred_plot else 1)


    # Add RSI or Normalize_MACD chart to the second row if available
    for indicator in indicators:
        if indicator == 'RSI' or indicator == 'Normalize_MACD':
            fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=2, col=1)
        else:
            if indicator not in chart_colors.keys():
                chart_colors[indicator] = chart_colors['Else']
            fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=1, col=1)


    if bound_hundred_plot: 
        #fig.update_yaxes(range=[0, 100], row=2, col=1)
        fig.add_shape(type="line", x0=min(dates), y0=50, x1=max(dates), y1=50, row=2, col=1, line=dict(color=chart_colors['shapes'], width=2))
        fig.add_shape(type="line", x0=min(dates), y0=60, x1=max(dates), y1=60, row=2, col=1, line=dict(color='#D90368', width=2))
        fig.add_shape(type="line", x0=min(dates), y0=40, x1=max(dates), y1=40, row=2, col=1, line=dict(color='#D90368', width=2))

    
    # Add buy/sell markers to the price chart
    buy_dates = [trade['buy_date'] for trade in trades]
    buy_prices = [trade['buy_price'] for trade in trades]
    buy_indices = [trade['buy_index'] for trade in trades]  
    buy_signals = [trade['buy_signals']['Buy_Signal'] for trade in trades] 

    sell_dates = [trade['sell_date'] for trade in trades]
    sell_prices = [trade['sell_price'] for trade in trades]
    sell_indices = [trade['sell_index'] for trade in trades]  
    sell_signals = [trade['sell_signals']['Sell_Signal'] for trade in trades] 

    ratios = [float(ratio) for ratio in json_data["stats"]["positions"]["all_ratios"]]

    # Hover texts for the markets
    buy_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Buy Signal: {buy_signal}" for index, price, date, buy_signal in zip(buy_indices, buy_prices, buy_dates, buy_signals)]
    sell_hover_texts = [f"Index: {index}<br>Price: {price}<br>Date: {date}<br>Ratio: {ratio}<br>Sell Signal: {sell_signal}" for index, price, date, ratio, sell_signal in zip(sell_indices, sell_prices, sell_dates, ratios, sell_signals)]

    # Plot buy/sell markers on the price chart
    fig.add_trace(go.Scatter(
        x=buy_dates, 
        y=buy_prices, 
        mode='markers', 
        name='Buy', 
        marker=dict(symbol='triangle-up', color='#16DB93', size=10),
        hovertext=buy_hover_texts,  
        hoverinfo='text'  
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=sell_dates, 
        y=sell_prices, 
        mode='markers', 
        name='Sell', 
        marker=dict(symbol='triangle-down', color='#EFEA5A', size=10),
        hovertext=sell_hover_texts,  
        hoverinfo='text' 
    ), row=1, col=1)

    # Update layout
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

    fig.show()

    directory = 'integrations/plotly/saved_results/'
    os.makedirs(directory, exist_ok=True)
    plot_filename = f'plot_{data_file}_{strategy}.html'
    fig.write_html(directory + plot_filename)
    #webbrowser.open(os.path.join(os.getcwd(), 'integrations', 'plotly', 'saved_results', plot_filename)) # save html file
