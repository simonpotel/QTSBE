import requests
import customtkinter as ctk
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import os

chart_colors = {
    "Price": "#6c7386", #gunmetal
    "MA_100": "#B8336A", #raspberry rose
    "MA_40": "#FF9B42", #sandy brown
    "MA_20": "#00A7E1", #picton blue
    "Test": "#C73E1D", #sinopia
    "RSI": "#9AB87A", #olivine
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

def plot_json_data_in_gui(json_data, root, data_combo, strategy_combo):
    """Plot JSON data in the GUI with two subplots."""
    dates, values = extract_dates_and_values(json_data['data'])
    trade_indices, trade_ratios = extract_trade_data(json_data['result'][1])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10), facecolor='#2b2b2b')

    plot_price_and_indicators(ax1, dates, values, json_data['result'][0], data_combo, strategy_combo)
    plot_trade_ratios(ax2, trade_indices, trade_ratios)

    fig.tight_layout()

    embed_plot_in_gui(fig, root)

def extract_dates_and_values(data):
    """Extract dates and values from the JSON data."""
    dates = []
    values = []
    date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]

    for entry in data:
        date = parse_date(entry[0], date_formats)
        if date:
            dates.append(date)
        value = parse_value(entry[1])
        if value is not None:
            values.append(value)

    return dates, values

def parse_date(date_str, date_formats):
    """Parse a date string using the provided date formats."""
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    print(f"Invalid date format: {date_str}")
    return None

def parse_value(value_str):
    """Parse a value string to a float."""
    try:
        return float(value_str)
    except ValueError:
        print(f"Invalid value format: {value_str}")
        return None

def extract_trade_data(trades):
    """Extract trade indices and ratios from the trade data."""
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios

def plot_price_and_indicators(ax, dates, values, indicators, data_combo, strategy_combo):
    """Plot the price and indicators on the given axis."""
    ax.set_facecolor('#2b2b2b')
    ax.plot(dates, values, color=chart_colors["Price"], linestyle='-', linewidth=2, label='Price')

    for indicator, indicator_values in indicators.items():
        if indicator != "RSI":
            values_indicator = [float(entry) if entry is not None else 0.0 for entry in indicator_values]
            ax.plot(dates, values_indicator, color=chart_colors[indicator], linestyle='-', linewidth=2, label=indicator.upper())

    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Value', color='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.set_title(f"{data_combo.get()} ({strategy_combo.get()})", color='white')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1)).set_visible(True)

def plot_trade_ratios(ax, trade_indices, trade_ratios):
    """Plot the trade ratios on the given axis."""
    ax.set_facecolor('#2b2b2b')
    ax.axhline(y=1, color='#2F4858', linestyle='--', linewidth=1, label='')
    ax.plot(trade_indices, trade_ratios, color='#F6AE2D', linestyle='-', linewidth=2, label='Trade Ratios')
    ax.set_xlabel('Trade Index', color='white')
    ax.set_ylabel('Ratio', color='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.set_title('Trade Ratios Over Time', color='white')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1)).set_visible(True)

    # cumulative ratios
    if len(trade_ratios) > 0:
        cumulative_ratios = [trade_ratios[0]]
        for i in range(1, len(trade_ratios)):
            cumulative_ratio = cumulative_ratios[i - 1] * trade_ratios[i]
            cumulative_ratios.append(cumulative_ratio)
        ax.plot(trade_indices, cumulative_ratios, color='#F26419', linestyle='-', linewidth=2, label='Cumulative Ratios')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 0.9)).set_visible(True)
        #print("Final Cumulative Ratio:", cumulative_ratios[-1])

        # adjust y-axis limits for better readability
        max_ratio = max(max(trade_ratios), max(cumulative_ratios))
        min_ratio = min(min(trade_ratios), min(cumulative_ratios))
        ax.set_ylim(min_ratio - 0.1, max_ratio + 0.1)
        ax.axhline(y=cumulative_ratios[-1], color='#2F4858', linestyle='--', linewidth=1)

def embed_plot_in_gui(fig, root):
    """embed the Matplotlib plot in the Tkinter GUI"""
    canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = tk.Frame(root)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    navigation_toolbar = NavigationToolbar2Tk(canvas, toolbar)
    navigation_toolbar.update()
    navigation_toolbar.configure(background='#2b2b2b')
    for item in navigation_toolbar.winfo_children():
        item.configure(bg='#2b2b2b')
