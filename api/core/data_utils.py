import math
import os
import h5py
import pandas as pd

def clean_nans(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value): return None
        return value
    elif isinstance(value, dict): return {k: clean_nans(v) for k, v in value.items()}
    elif isinstance(value, list): return [clean_nans(v) for v in value]
    elif isinstance(value, tuple): return tuple(clean_nans(v) for v in value)
    return value

def get_h5_store():
    path = "data/bank/qtsbe_data.h5"
    if os.path.exists(path): return h5py.File(path, 'r')
    return None

def list_keys():
    f = get_h5_store()
    if not f: return []
    keys = list(f.keys())
    f.close()
    return keys

def get_data(pair, limit=None):
    try:
        f = get_h5_store()
        if f and pair in f:
            data = f[pair][:] if limit is None else f[pair][-limit:]
            f.close()
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
            return df.values.tolist()
    except Exception: pass
    return []
