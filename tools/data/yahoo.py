import os
import pandas as pd
import yfinance as yf
import h5py
import numpy as np
from loguru import logger

class YahooAPI:
    def __init__(self, h5_path='data/bank/qtsbe_data.h5'):
        self.h5_path = h5_path
        os.makedirs(os.path.dirname(self.h5_path), exist_ok=True)

    def update_ohlcv(self, ticker, interval='1d'):
        key = f"Yahoo_{ticker.replace('/', '_')}_{interval}"
        last_ts = None
        
        if os.path.exists(self.h5_path):
            try:
                with h5py.File(self.h5_path, 'r') as f:
                    if key in f:
                        data = f[key][:]
                        if len(data) > 0:
                            last_ts = data[-1][0]
            except Exception: pass

        try:
            params = {"tickers": ticker, "interval": interval, "progress": False}
            if last_ts:
                dt = pd.to_datetime(last_ts, unit='ms')
                params["start"] = dt
            
            df = yf.download(**params)
            if df.empty: return
            
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.reset_index().rename(columns={'Date': 'timestamp', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
            df['timestamp'] = pd.to_datetime(df['timestamp']).astype('int64') // 10**6
            
            if last_ts:
                df = df[df['timestamp'] > last_ts]
            
            if df.empty: return
            
            new_data = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values
            
            with h5py.File(self.h5_path, 'a') as f:
                if key in f:
                    old_data = f[key][:]
                    combined = np.vstack([old_data, new_data])
                    del f[key]
                    f.create_dataset(key, data=combined, compression="gzip")
                else:
                    f.create_dataset(key, data=new_data, compression="gzip", maxshape=(None, 6))
            
            logger.info(f"Yahoo:{ticker} updated")
        except Exception as e:
            logger.error(f"Yahoo:{ticker} error: {e}")
        finally:
            pass
