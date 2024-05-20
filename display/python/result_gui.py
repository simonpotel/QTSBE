import requests
import customtkinter as ctk
import json
from datetime import datetime

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

        text_frame = ctk.CTkFrame(new_window, corner_radius=10)
        text_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        text_widget = ctk.CTkTextbox(text_frame, wrap="none")
        text_widget.pack(fill="both", expand=True)
        
        json_data = json.loads(response.text)
        formatted_json = json.dumps(json_data, indent=4)
        text_widget.insert("1.0", formatted_json)
        
        save_button = ctk.CTkButton(new_window, text="Save Request Json", command=lambda: save_to_file(formatted_json))
        save_button.pack(pady=10)
        
    except requests.RequestException as e:
        print("Request failed:", e)

def save_to_file(content):
    try:
        content_dict = json.loads(content) 
        filename = f"display/python/saved_results/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{content_dict['pair']}_{content_dict['strategy']}.json"
        
        with open(filename, "w") as file:
            file.write(content)
        print("Content saved")
    except Exception as e:
        print("Failed to save content:", e)
