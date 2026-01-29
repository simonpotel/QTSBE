import os
import h5py
import pandas as pd
from loguru import logger

def get_file_data(pair):
    try:
        h5_path = "data/bank/qtsbe_data.h5"
        if os.path.exists(h5_path):
            with h5py.File(h5_path, 'r') as f:
                if pair in f:
                    data = f[pair][:]
                    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
                    return df.values.tolist()
    except Exception as e:
        logger.error(f"Error reading {pair} from HDF5: {e}")
    return []