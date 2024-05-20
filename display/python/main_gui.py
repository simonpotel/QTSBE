import os
import customtkinter as ctk
from result_gui import fetch_and_show_data

#This file contains the main menu code for data selection, 
#strategy selection and a button for loading the request and displaying the results.

def list_files_in_directory(directory):
    """Get files of a directory without their extension"""
    return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def show_toload(data_combo, strategy_combo, root):
    print("Selected file:", data_combo.get())
    print("Selected option:", strategy_combo.get())
    fetch_and_show_data(data_combo, strategy_combo, root)

ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # "blue", "dark-blue", "green"

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
data_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("data/"), width=300)
data_combo.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="ew")

# strategy selector
label_strategy = ctk.CTkLabel(frame, text="Strategy:")
label_strategy.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
strategy_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("api/strategies/"), width=300)
strategy_combo.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="ew")

# button that make a request in result_gui.py to the API and print the data
load_button = ctk.CTkButton(frame, text="Load", command=lambda: show_toload(data_combo, strategy_combo, root))
load_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)

root.mainloop()
