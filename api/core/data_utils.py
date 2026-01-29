import math
import os
import h5py
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H5_PATH = os.path.join(ROOT_DIR, "data", "bank", "qtsbe_data.h5")

def clean_nans(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value): return None
        return value
    elif isinstance(value, dict): return {k: clean_nans(v) for k, v in value.items()}
    elif isinstance(value, list): return [clean_nans(v) for v in value]
    elif isinstance(value, tuple): return tuple(clean_nans(v) for v in value)
    return value

def list_keys():
    try:
        if not os.path.exists(H5_PATH): return []
        with h5py.File(H5_PATH, 'r') as f:
            return list(f.keys())
    except Exception: return []

def get_data(pair, limit=None):
    try:
        if not os.path.exists(H5_PATH): return []
        with h5py.File(H5_PATH, 'r') as f:
            if pair not in f: return []
            data = f[pair][:] if limit is None else f[pair][-limit:]
            
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        return df.values.tolist()
    except Exception: return []
