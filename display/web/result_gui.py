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

def fetch_and_show_data(data_combo, strategy_combo):
    data_file = data_combo.get()
    strategy = strategy_combo.get()
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        display_results_in_new_window(response.text, data_combo, strategy_combo, url)  
    except requests.RequestException as e:
        print("Request failed:", e)

def display_results_in_new_window(response_text, data_combo, strategy_combo, url):
    """display the fetched results in a new window with a plot and JSON data"""
    new_window = ctk.CTkToplevel()  
    new_window.title("Result: " + url)
    new_window.geometry("1200x800")

    text_frame, graph_frame = create_frames(new_window)

    json_data = json.loads(response_text)
    display_json_data(json_data, text_frame)
    add_save_button(text_frame, json_data)

    plot_json_data_in_gui(json_data, graph_frame, data_combo, strategy_combo)

def create_frames(new_window):
    """create and pack the text and graph frames in the new window."""
    text_frame = ctk.CTkFrame(new_window, corner_radius=10)
    text_frame.pack(fill="both", expand=True, side="left")
    graph_frame = ctk.CTkFrame(new_window, corner_radius=10)
    graph_frame.pack(fill="both", expand=True, side="right")
    return text_frame, graph_frame

def display_json_data(json_data, text_frame):
    """display formatted JSON request data in a text widget."""
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
        os.makedirs('display/web/saved_results/', exist_ok=True)
        filename = generate_filename(content)
        with open(filename, "w") as file:
            file.write(json.dumps(content, indent=4))
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)

def generate_filename(content):
    """generate a filename based on the current timestamp, pair, and strategy."""
    return f"display/web/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content['pair']}_{content['strategy']}.json"

def extract_trade_data(trades):
    """Extract trade indices and ratios from the trade data."""
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios

def plot_json_data_in_gui(json_data, graph_frame, data_combo, strategy_combo):
    """Plot JSON data in the GUI with candlestick chart, RSI chart (if available), and trade ratios."""
    dates, opens, highs, lows, closes = extract_ohlc_data(json_data['data'])
    indicators = extract_indicators(json_data)
    trade_indices, trade_ratios = extract_trade_data(json_data['result'][1])
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
        cumulative_ratios = [trade_ratios[0]]
        for i in range(1, len(trade_ratios)):
            cumulative_ratio = cumulative_ratios[i - 1] * trade_ratios[i]
            cumulative_ratios.append(cumulative_ratio)
        fig.add_trace(go.Scatter(x=trade_indices, y=cumulative_ratios, mode='lines', name='Cumulative Ratios', line=dict(color=chart_colors['MA_100'])), row=1, col=2)

    # layout
    fig.update_layout(title=f"{data_combo.get()} ({strategy_combo.get()})",
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

    os.makedirs('display/web/saved_results/', exist_ok=True)
    plot_filename = 'display/web/saved_results/plot.html'
    fig.write_html(plot_filename)
    webbrowser.open(os.path.join(os.getcwd(), 'display', 'web', 'saved_results', 'plot.html'))

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