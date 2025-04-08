import sys
import os
import pandas as pd
import plotly.graph_objects as go
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_fibonacci_retracement_levels(data, start_index, end_index):

    if start_index < 0 or end_index >= len(data) or start_index >= end_index:
        # Increment end_index if it is equal to start_index and within bounds
        if start_index == end_index and end_index + 1 < len(data):
            end_index += 1
        else:
            raise ValueError("Invalid indices. Ensure 0 <= start_index < end_index < len(prices).")

    low_price = min([float(row[3]) for row in data[start_index:end_index + 1]])
    high_price = max([float(row[2]) for row in data[start_index:end_index + 1]])
    price_range = high_price - low_price
    retracement_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    retracement_prices = {f"{level * 100:.1f}%": high_price - (price_range * level) for level in retracement_levels}

    return retracement_prices

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
pair = "Binance_SOLUSDC_1d"
data = get_file_data(pair) 
if not data:
    sys.exit("Data retrieval failed.")
    
first_index = 0
second_index = len(data)//2
fibonacci_retracement_levels = get_fibonacci_retracement_levels(data, first_index, second_index)
fig = go.Figure(data=[go.Candlestick(
    x=[index for index in range(first_index, second_index + 1, 1)],  
    open=[entry[1] for entry in data[first_index:second_index + 1]],
    high=[entry[2] for entry in data[first_index:second_index + 1]],
    low=[entry[3] for entry in data[first_index:second_index + 1]],
    close=[entry[4] for entry in data[first_index:second_index + 1]]
)])
levels = list(fibonacci_retracement_levels.keys())
for level, color, name in zip(fibonacci_retracement_levels.values(), ['blue', 'green', 'red', 'orange', 'purple', 'magenta'], levels):
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