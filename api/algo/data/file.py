import pandas as pd
from api import logger

def get_file_data(pair):
    file_path = f"data/bank/{pair}.csv"  # path of the CSV file that contents data of the pair
    try:
        csv_data = pd.read_csv(file_path).to_dict(orient='records')  # reading CSV data into dictionary format
    except FileNotFoundError:  # log error if file not found and return empty list
        logger.error(f"The file {pair}.csv was not found.")
        return []
    data = [[str(row["timestamp"]), str(row["open"]), str(row["high"]), str(row["low"]), str(row["close"]), str(row["volume"])] for row in csv_data] # transforming CSV data into a list of lists
    for row in data:
        for i in range(1, len(row)):
            row[i] = float(row[i].replace(',', ''))
    #data.reverse() # reversing the order of data (because in the files that we have stocked they data is from recent to old)
    logger.debug(f"Data was successfully retrieved. {pair}")
    return data # return the data (list of lists) with datetime and price, from older to latest value
