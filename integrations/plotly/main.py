import sys
from utils.api_requests import fetch_and_show_data

def main():
    if len(sys.argv) < 3:
        print("Usage: main.py -data <data_file> -strategy <strategy_file> [-start_ts <start_timestamp>] [-end_ts <end_timestamp>] [-multi_positions <True/False>]")
        sys.exit(1)

    data = None
    strategy = None
    start_ts = "2000-01-01 00:00:00"
    end_ts = "9999-01-01 00:00:00"
    multi_positions = "True"

    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i] == "-data":
            data = args[i+1]
        elif args[i] == "-strategy":
            strategy = args[i+1]
        elif args[i] == "-start_ts":
            start_ts = args[i+1]
        elif args[i] == "-end_ts":
            end_ts = args[i+1]
        elif args[i] == "-multi_positions":
            multi_positions = args[i+1]

    if data and strategy:
        fetch_and_show_data(data, strategy, start_ts, end_ts, multi_positions)
    else:
        print("Error: -data and -strategy arguments are required")
        sys.exit(1)

if __name__ == "__main__":
    main()
