import requests
import customtkinter as ctk
import json
from datetime import datetime
import plotly.graph_objs as go
import webbrowser
import os
from plotly.subplots import make_subplots

chart_colors = {
    "price": "#6c7386", #gunmetal
    "mm_100": "#B8336A", #raspberry rose
    "mm_40": "#FF9B42", #sandy brown
    "mm_20": "#00A7E1", #picton blue
    "test": "#C73E1D", #sinopia
    "rsi": "#9AB87A", #olivine
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
        os.makedirs('display/python/saved_results/', exist_ok=True)
        filename = generate_filename(content)
        with open(filename, "w") as file:
            file.write(json.dumps(content, indent=4))
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)

def generate_filename(content):
    """generate a filename based on the current timestamp, pair, and strategy."""
    return f"display/python/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content['pair']}_{content['strategy']}.json"

def plot_json_data_in_gui(json_data, graph_frame, data_combo, strategy_combo):
    """Plot JSON data in the GUI with candlestick chart and RSI chart if available."""
    dates, opens, highs, lows, closes = extract_ohlc_data(json_data['data'])
    indicators = extract_indicators(json_data)
    to_plot = 1
    if 'rsi' in indicators: to_plot += 1

    if not dates or not opens or not highs or not lows or not closes:
        print("Error: OHLC data is missing or empty")
        return

    # subplot grid
    fig = make_subplots(rows=to_plot, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # candlestick chart to the first subplot
    fig.add_trace(go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes), row=1, col=1)

    # layout
    fig.update_layout(title=f"{data_combo.get()} ({strategy_combo.get()})",
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)

    for indicator in indicators:
        if indicator == 'rsi':
            fig.add_trace(go.Scatter(x=dates, y=indicators['rsi'], mode='lines', name='RSI', line=dict(color=chart_colors['rsi'])), row=2, col=1)
        else:
            fig.add_trace(go.Scatter(x=dates, y=indicators[indicator], mode='lines', name=indicator, line=dict(color=chart_colors[indicator])), row=1, col=1)


    # plot
    plot_filename = 'temp_plot.html'
    fig.write_html(plot_filename)
    webbrowser.open(plot_filename)

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