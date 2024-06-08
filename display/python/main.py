import os
import sys
import customtkinter as ctk
from result_gui import fetch_and_show_data

def list_files_in_directory(directory, extension):
    """Get files of a directory and its subdirectories without their extension"""
    files = []
    for root, dirs, files_in_dir in os.walk(directory):
        for file_name in files_in_dir:
            if file_name.endswith(extension):  # Only consider files with the specified extension
                relative_path = os.path.relpath(os.path.join(root, file_name), directory)
                name_without_extension = os.path.splitext(relative_path)[0].replace(os.sep, '_')
                files.append(name_without_extension)
    return files or ['None']

def main(data=None, strategy=None):
    if data and strategy:
        fetch_and_show_data(data, strategy)
    else:
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
        data_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("data/bank/", ".csv"), width=300)
        data_combo.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="ew")

        # strategy selector
        label_strategy = ctk.CTkLabel(frame, text="Strategy:")
        label_strategy.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        strategy_combo = ctk.CTkComboBox(frame, values=list_files_in_directory("api/strategies/", ".py"), width=300)
        strategy_combo.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="ew")

        # button that makes a request in result_gui.py to the API and print the data
        load_button = ctk.CTkButton(frame, text="Load", command=lambda: fetch_and_show_data(data_combo.get(), strategy_combo.get()))
        load_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))

        root.mainloop()

if __name__ == "__main__":
    data_arg = sys.argv[1] if len(sys.argv) > 1 else None
    strategy_arg = sys.argv[2] if len(sys.argv) > 2 else None
    main(data_arg, strategy_arg)
