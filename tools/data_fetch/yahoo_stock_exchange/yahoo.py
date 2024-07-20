import yfinance as yf
import os

def download_and_save(tickers, interval='1d'):
    data = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, interval=interval)
            stock_data.reset_index(inplace=True)
            stock_data = stock_data.rename(columns={
                'Date': 'timestamp',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            stock_data = stock_data.drop(columns=['Adj Close'])

            data[ticker] = stock_data
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")
    
    output_dir = 'data/bank/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for ticker, df in data.items():
        df.to_csv(f'{output_dir}{ticker}_{interval}.csv', index=False)

