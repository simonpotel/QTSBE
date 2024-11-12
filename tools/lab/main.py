import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import os
import glob
import json


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QTSBE Lab")

        self.api_source_label = tk.Label(self, text="API Source")
        self.api_source_label.grid(row=0, column=0, padx=10, pady=10)
        self.api_source_combo = ttk.Combobox(self, values=["Yahoo", "Binance"])
        self.api_source_combo.grid(row=0, column=1, padx=10, pady=10)
        self.api_source_combo.bind("<<ComboboxSelected>>", self.update_pairs)

        self.pair_label = tk.Label(self, text="Trading Pair")
        self.pair_label.grid(row=1, column=0, padx=10, pady=10)
        self.pair_combo = ttk.Combobox(self)
        self.pair_combo.grid(row=1, column=1, padx=10, pady=10)

        self.timeframe_label = tk.Label(self, text="Timeframe")
        self.timeframe_label.grid(row=2, column=0, padx=10, pady=10)
        self.timeframe_combo = ttk.Combobox(self, values=["1d", "1h"])
        self.timeframe_combo.grid(row=2, column=1, padx=10, pady=10)

        self.strategy_label = tk.Label(self, text="Strategy")
        self.strategy_label.grid(row=3, column=0, padx=10, pady=10)
        self.strategy_combo = ttk.Combobox(self, values=self.load_strategies())
        self.strategy_combo.grid(row=3, column=1, padx=10, pady=10)

        self.load_button = tk.Button(
            self, text="Load", command=self.load_request)
        self.load_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.response_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=60, height=20)
        self.response_text.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10)

    def load_pairs(self):
        pairs = set()
        bank_path = "data/bank"
        for file_name in os.listdir(bank_path):
            if file_name.startswith("Binance_") or file_name.startswith("Yahoo_"):
                pair = file_name.split('_')[1]
                pairs.add(file_name.split('_')[0] + "_" + pair)
        return list(pairs)

    def update_pairs(self, event):
        api_source = self.api_source_combo.get()
        pairs = self.load_pairs()
        filtered_pairs = [pair.split('_')[1]
                          for pair in pairs if pair.startswith(api_source)]
        self.pair_combo['values'] = filtered_pairs

    def load_strategies(self):
        strategies = []
        strategies_path = "api/strategies"
        for file_path in glob.glob(os.path.join(strategies_path, '**/*.py'), recursive=True):
            if file_path.endswith("__init__.py"):
                continue
            relative_path = os.path.relpath(file_path, strategies_path)
            strategy_name = relative_path.replace(
                os.sep, '_').rsplit('.', 1)[0]
            strategies.append(strategy_name)
        return strategies

    def load_request(self):
        api_source = self.api_source_combo.get()
        pair = self.pair_combo.get()
        timeframe = self.timeframe_combo.get()
        strategy = self.strategy_combo.get()

        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, f"Loading {api_source} {
                                  pair} {timeframe} {strategy}...\n")

        url = f"http://127.0.0.1:5000/QTSBE/{api_source}_{
            pair}_{timeframe}/{strategy}?details=False"
        response = requests.get(url)
        self.response_text.delete(1.0, tk.END)
        try:
            data = response.json()
            self.response_text.insert(tk.END, json.dumps(data, indent=4))
        except requests.exceptions.JSONDecodeError:
            self.response_text.insert(
                tk.END, f"Invalid JSON response: {response.text}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
