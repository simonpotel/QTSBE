import sys
import os
import pandas as pd
import plotly.graph_objects as go
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.algo.indicators.fibonacci_retracements import get_fibonacci_retracement_levels

def get_file_data(pair):
    file_path = f"data/bank/{pair}.csv"
    try:
        csv_data = pd.read_csv(file_path).to_dict(orient='records')
    except FileNotFoundError:
        print(f"The file {pair}.csv was not found.")
        return []
    
    data = [[str(row["timestamp"]), str(row["open"]), str(row["high"]), str(row["low"]), str(row["close"]), str(row["volume"])] for row in csv_data]
    print(f"Data was successfully retrieved for {pair}.")
    return data

pair = "Binance_BTCUSDT_1d"
data = get_file_data(pair) 
prices = [float(entry[1].replace(',', ''))  for entry in data] 
fibonacci_retracement_levels = get_fibonacci_retracement_levels(prices, 0, len(data)-1)
fig = go.Figure(data=[go.Candlestick(
    x=list(range(len(data))),  
    open=[entry[1] for entry in data],
    high=[entry[2] for entry in data],
    low=[entry[3] for entry in data],
    close=[entry[4] for entry in data]
)])

colors = ['blue', 'green', 'red', 'orange', 'purple', 'magenta']
levels = list(fibonacci_retracement_levels.keys())
for level, color, name in zip(fibonacci_retracement_levels.values(), colors, levels):
    fig.add_hline(y=level, line_dash="dash", line_color=color, name=f"Fib Retracement: {name}")
    fig.add_annotation(
        xref="paper",
        yref="y",
        x=1.02,
        y=level,
        text=f"Fib Retracement: {name}",
        showarrow=False
    )
fig.update_layout(
    title=f"{pair} : Fibonacci Retracement Levels",
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False,
    plot_bgcolor='#161a25', 
    paper_bgcolor='#161a25',  
    font=dict(color='white'),  
    yaxis=dict(gridcolor='#6c7386'),  
    xaxis=dict(gridcolor='#6c7386'),  
)
fig.show()
