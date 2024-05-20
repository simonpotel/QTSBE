import os
import customtkinter as ctk

def list_files_in_directory(directory):
    """Get files of a directory without their extension"""
    return [os.path.splitext(f)[0] for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def show_toload():
    print("Selected file:", data_combo.get())
    print("Selected option:", strategy_combo.get())

ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("green")  # "blue", "dark-blue", "green"

root = ctk.CTk()
root.title("QTSBE")

root.geometry("420x185")  # Set a default size for the window

frame = ctk.CTkFrame(root, corner_radius=10)
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

label_data = ctk.CTkLabel(frame, text="Data:")
label_data.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
data_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("data/"), width=300)
data_combo.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="ew")

label_strategy = ctk.CTkLabel(frame, text="Strategy:")
label_strategy.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
strategy_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("api/strategies/"), width=300)
strategy_combo.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="ew")

load_button = ctk.CTkButton(frame, text="Load", command=show_toload)
load_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))

# Configure column weights to ensure proper resizing
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)

root.mainloop()
