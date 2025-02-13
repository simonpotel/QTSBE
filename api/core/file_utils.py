import os
import pandas as pd
from loguru import logger

def get_file_data(pair):
    try:
        bank_path = "data/bank"
        filepath = os.path.join(bank_path, f"{pair}.csv")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if pair.startswith('Yahoo_'):
            df = pd.read_csv(filepath, skiprows=[1])
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        else:
            df = pd.read_csv(filepath)
            
        return df.values.tolist()
        
    except Exception as e:
        logger.error(f"Error reading file for pair {pair}: {str(e)}")
        return [] 