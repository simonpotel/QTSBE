import os
import pandas as pd
from loguru import logger

def find_most_recent_date(filepath):
    try:
        df = pd.read_csv(filepath)
        if not df.empty:
            # Convertir la colonne 'timestamp' en datetime si elle ne l'est pas déjà
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Trouver la date la plus récente dans la colonne 'timestamp'
            most_recent_date = df['timestamp'].max()
            return most_recent_date
        else:
            return None
    except Exception as e:
        logger.error(f"Error processing {filepath}: {str(e)}")
        return None

def main():
    bank_dir = 'data/bank'
    logger.info(f"Searching for the most recent date in CSV files located in {bank_dir}")
    
    for filename in os.listdir(bank_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(bank_dir, filename)
            most_recent_date = find_most_recent_date(filepath)
            if most_recent_date is not None:
                logger.info(f"File: {filename}, Most Recent Date: {most_recent_date}")
    
    logger.info("Process completed.")

if __name__ == "__main__":
    main()