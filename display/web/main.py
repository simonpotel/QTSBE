import os
import customtkinter as ctk
from result_gui import fetch_and_show_data

def list_files_in_directory(directory):
    """Get files of a directory without their extension"""
    try:
        return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except:
        return ['None']

ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("dark-blue")  # "blue", "dark-blue", "green"

# create the main window QTSBE
root = ctk.CTk()
root.title("QTSBE")

root.geometry("420x185")

# pack grid for the items
frame = ctk.CTkFrame(root, corner_radius=10)
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# data selector
label_data = ctk.CTkLabel(frame, text="Data:")
label_data.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
data_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("data/bank/"), width=300)
data_combo.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="ew")

# strategy selector
label_strategy = ctk.CTkLabel(frame, text="Strategy:")
label_strategy.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
strategy_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("api/strategies/"), width=300)
strategy_combo.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="ew")

# button that make a request in result_gui.py to the API and print the data
load_button = ctk.CTkButton(frame, text="Load", command=lambda: fetch_and_show_data(data_combo, strategy_combo))
load_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))


root.mainloop()