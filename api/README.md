### QTSBE/api

This directory contains all the code for the API, including the algorithmic logic, statistical system, and all the strategies utilized by the API.

#### Getting Started
To start the Flask API, navigate to the QTSBE directory and run the following command:

```bash
python api/api.py
```

#### Debug Mode
You can start the API in debug mode to access debugging information. 

#### Logs
Logs for the API can be found in the following directory:

```
QTSBE/logs/
```

Feel free to explore and analyze the logs for further insight into the API's behavior.

### QTSBE/api/algo
This directory houses all the algorithmic code utilized within the API.

#### Data Retrieval
The `api/algo/data/file.py` module enables the retrieval of data for the desired trading pair from the API request in the database.

#### Indicators
The `api/algo/indicators` directory contains all the indicators used for technical analysis. As a technical choice, I've opted not to import another library and have developed them from scratch.
Feel free to explore the code for further understanding of the algorithmic processes and data handling within the API.