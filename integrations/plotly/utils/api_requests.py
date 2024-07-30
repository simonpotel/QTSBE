import requests
import json
import os
from datetime import datetime
from utils.plots import plot_json_data_in_gui

def fetch_and_show_data(data_file, strategy, start_ts, end_ts, multi_positions):
    url = f"http://127.0.0.1:5000/QTSBE/{data_file}/{strategy}?start_ts={start_ts}&end_ts={end_ts}&multi_positions={multi_positions}&details=True"

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        plot_json_data_in_gui(json_data, data_file, strategy)
    except requests.RequestException as e:
        print("Request failed:", e)

def save_to_file(content):
    try:
        os.makedirs('integrations/plotly/saved_results/', exist_ok=True)
        filename = generate_filename(content)
        with open(filename, "w") as file:
            file.write(json.dumps(content, indent=4))
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)

def generate_filename(content):
    return f"integrations/plotly/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content['pair']}_{content['strategy']}.json"

def extract_trade_data(trades):
    trade_indices = list(range(1, len(trades) + 1))
    trade_ratios = [trade['ratio'] for trade in trades if 'ratio' in trade]
    return trade_indices, trade_ratios
