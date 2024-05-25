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
    "price": "#6c7386", #gunmetal
    "mm_100": "#B8336A", #raspberry rose
    "mm_40": "#FF9B42", #sandy brown
    "mm_20": "#00A7E1", #picton blue
    "test": "#C73E1D", #sinopia
    "rsi": "#9AB87A", #olivine
}

def fetch_and_show_data(data_combo, strategy_combo, root):
    data_file = data_combo.get()
    strategy = strategy_combo.get()
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        new_window = ctk.CTkToplevel(root)
        new_window.title("Result: " + url)
        new_window.geometry("1200x800")

        # divide window into two frames
        text_frame = ctk.CTkFrame(new_window, corner_radius=10)
        text_frame.pack(fill="both", expand=True, side="left")
        graph_frame = ctk.CTkFrame(new_window, corner_radius=10)
        graph_frame.pack(fill="both", expand=True, side="right")
        
        # json data widget
        text_widget = ctk.CTkTextbox(text_frame, wrap="none")
        text_widget.pack(fill="both", expand=True)
        
        json_data = json.loads(response.text)
        formatted_json = json.dumps(json_data, indent=4)
        text_widget.insert("1.0", formatted_json)
        
        save_button = ctk.CTkButton(text_frame, text="Save Request Json", command=lambda: save_to_file(formatted_json))
        save_button.pack(pady=10)
        
        # plot graph
        plot_json_data_in_gui(json_data, graph_frame, data_combo, strategy_combo)
        tk.mainloop()

    except requests.RequestException as e:
        print("Request failed:", e)


def save_to_file(content):
    try:
        os.makedirs('display/python/saved_results/', exist_ok=True)
        content_dict = json.loads(content) 
        filename = f"display/python/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content_dict['pair']}_{content_dict['strategy']}.json"
        
        with open(filename, "w") as file:
            file.write(content)
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)

def plot_json_data_in_gui(json_data, root, data_combo, strategy_combo):
    # extracting dates and values from the JSON data
    data = json_data['data']
    dates = []
    values = []

    date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]  # date formats expected

    for entry in data:
        date_parsed = False
        for fmt in date_formats:
            try:
                date = datetime.strptime(entry[0], fmt)
                dates.append(date)
                date_parsed = True
                break
            except ValueError:
                continue
        if not date_parsed:
            print(f"Invalid date format: {entry[0]}")

        try:
            value = float(entry[1])
            values.append(value)
        except ValueError:
            print(f"Invalid value format: {entry[1]}")

    if not dates:
        print("No valid dates found. Cannot plot the data.")
        return
    if not values:
        print("No valid values found. Cannot plot the data.")
        return

    # plotting the data
    fig = plt.Figure(figsize=(8, 6), facecolor='#2b2b2b')  # set background color for the whole figure
    ax = fig.add_subplot(111, facecolor='#2b2b2b')  # set background color for the subplot
    
    lines = []  
    labels = [] 
    
    line, = ax.plot(dates, values, color=chart_colors["price"], linestyle='-', linewidth=2, label='Price')  # set line color to green
    lines.append(line)
    labels.append('Price')
    
    for indicator in json_data['result'][0].keys():
        if indicator != "rsi":
            values_indicator = [float(entry) if entry is not None else 0.0 for entry in json_data['result'][0][indicator]]
            line, = ax.plot(dates, values_indicator, color=chart_colors[indicator], linestyle='-', linewidth=2, label=indicator.upper())
            lines.append(line)
            labels.append(indicator.upper())
    
    ax.set_xlabel('Date', color='white') 
    ax.set_ylabel('Value', color='white')
    ax.tick_params(axis='y', colors='white')  

    ax.set_title(f"{data_combo.get()} ({strategy_combo.get()})", color='white')  

    # format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.tick_params(axis='x', rotation=45, colors='white')  

    legend = ax.legend(lines, labels, loc='upper left', bbox_to_anchor=(1, 1))  
    legend.set_visible(True)  

    fig.tight_layout()

    # embed the plot into a Tkinter window
    canvas = tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # toolbar for navigation
    toolbar = tk.Frame(root)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    toolbar.update()

    # navigation buttons (from matplotlib)
    navigation_toolbar = NavigationToolbar2Tk(canvas, toolbar)
    navigation_toolbar.update()
    navigation_toolbar.configure(background='#2b2b2b')  
    for item in navigation_toolbar.winfo_children():
        item.configure(bg='#2b2b2b')
