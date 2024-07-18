import requests
import customtkinter as ctk
import json
from datetime import datetime
import plotly.graph_objs as go
import webbrowser
import os
from plotly.subplots import make_subplots

chart_colors = {
    "Price": "#6c7386", #gunmetal (grey)
    "MA_100": "#B8336A", #raspberry rose (pink)
    "MA_40": "#FF9B42", #sandy brown (orange)
    "MA_20": "#F4D35E", #naples yellow (yellow)
    "Test": "#C73E1D", #sinopia (red)
    "RSI": "#9AB87A", #olivine (green)
    "EMA": "#F0A7A0", #melon (~red light)
    "EMA_MACD": "#F0A7A0", #melon (~red light)
    "MACD": "#5E4AE3", #majorelle blue (blue/purple)
    "Normalize_MACD": "#947BD3", #tropical indigo,
    "Bollinger_Lower": "#A682FF", #forest green
    "Bollinger_Rolling": "#A682FF",#forest green
    "Bollinger_Upper": "#A682FF", #forest green
}

def fetch_and_show_data(data_file, strategy, start_ts, end_ts, multi_positions):
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}?start_ts={start_ts}&end_ts={end_ts}&multi_positions={multi_positions}&details=True"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        plotly_results_in_new_window(response.text, data_file, strategy, url)  
    except requests.RequestException as e:
        print("Request failed:", e)

def plotly_results_in_new_window(response_text, data_file, strategy, url):
    """displplotlyay the fetched results in a new window with a plot and JSON data"""
    new_window = ctk.CTkToplevel()  
    new_window.title("Result: " + url)
    new_window.geometry("1200x800")

    text_frame, graph_frame = create_frames(new_window)

    json_data = json.loads(response_text)
    plotly_json_data(json_data, text_frame)
    add_save_button(text_frame, json_data)

    plot_json_data_in_gui(json_data, graph_frame, data_file, strategy)

def create_frames(new_window):
    """create and pack the text and graph frames in the new window."""
    text_frame = ctk.CTkFrame(new_window, corner_radius=10)
    text_frame.pack(fill="both", expand=True, side="left")
    graph_frame = ctk.CTkFrame(new_window, corner_radius=10)
    graph_frame.pack(fill="both", expand=True, side="right")
    return text_frame, graph_frame

def plotly_json_data(json_data, text_frame):
    """plotly formatted JSON request data in a text widget."""
    text_widget = ctk.CTkTextbox(text_frame, wrap="none")
    text_widget.pack(fill="both", expand=True)
    formatted_json = json.dumps(json_data, indent=4)
    text_widget.insert("1.0", formatted_json)

def add_save_button(text_frame, json_data):
    """add a button to save JSON data to a file."""
    save_button = ctk.CTkButton(text_frame, text="Save Request Json", command=lambda: save_to_file(json_data))
    save_button.pack(pady=10)

def save_to_file(content):
    """save JSON content to a file."""
    try:
        os.makedirs('integrations/plotly/saved_results/', exist_ok=True)
        filename = generate_filename(content)
        with open(filename, "w") as file:
            file.write(json.dumps(content, indent=4))
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)

def generate_filename(content):
    """generate a filename based on the current timestamp, pair, and strategy."""
    return f"integrations/plotly/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content['pair']}_{content['strategy']}.json"

def extract_trade_data(trades):
    """Extract trade indices and ratios from the trade data."""
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios

def plot_json_data_in_gui(json_data, graph_frame, data_file, strategy):
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
        cumulative_ratios = [float(cumultative_ratio) for cumultative_ratio in json_data["stats"]["positions"]["cumulative_ratios"]]
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


    # layout
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
