import ccxt
import pandas as pd
import h5py
import os
import numpy as np
from loguru import logger

class BinanceAPI:
    def __init__(self, h5_path='data/bank/qtsbe_data.h5'):
        self.exchange = ccxt.binance()
        self.h5_path = h5_path
        os.makedirs(os.path.dirname(self.h5_path), exist_ok=True)

    def update_ohlcv(self, symbol, timeframe='1d'):
        key = f"Binance_{symbol.replace('/', '')}_{timeframe}"
        since_ts = self.exchange.parse8601('2000-01-01T00:00:00Z')
        
        if os.path.exists(self.h5_path):
            try:
                with h5py.File(self.h5_path, 'r') as f:
                    if key in f:
                        data = f[key][:]
                        if len(data) > 0:
                            since_ts = int(data[-1][0]) 
            except Exception: pass

        try:
            new_ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since=since_ts)
            if not new_ohlcv: return
            
            new_data = np.array(new_ohlcv)
            
            with h5py.File(self.h5_path, 'a') as f:
                if key in f:
                    old_data = f[key][:]
                    if len(old_data) > 0 and len(new_data) > 0:
                        if old_data[-1][0] == new_data[0][0]:
                             new_data = new_data[1:]
                    
                    if len(new_data) > 0:
                        combined = np.vstack([old_data, new_data])
                        del f[key]
                        f.create_dataset(key, data=combined, compression="gzip")
                else:
                    f.create_dataset(key, data=new_data, compression="gzip", maxshape=(None, 6))
                
            logger.info(f"Binance:{symbol} updated")
        except Exception as e:
            logger.error(f"Binance:{symbol} error: {e}")
