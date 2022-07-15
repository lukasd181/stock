import pandas
import csv
# from Fetcher.config import API_KEY
from polygon import StocksClient
from datetime import datetime
import time
# datetime.now().strftime("%Y-%m-%d")
API_KEY = '1vGv44JgWWAnpRo0toD5mAcCfJ9ZIjx9'
LIMIT = 60000
FROM_DATE = "2016-01-01"
TIMESPAN = "day"
TO_DATE = "2022-06-30"

def get_historical_data(symbol: str, from_date: str = FROM_DATE, timespan: str = TIMESPAN, limit:int = LIMIT,full_range=True):
    client = StocksClient(
        api_key=API_KEY,
    )
    return client.get_aggregate_bars(
        symbol= symbol,
        from_date= from_date,
        to_date= TO_DATE,
        timespan=timespan,
        limit=limit,
        sort="desc"
    )

def get_recent_historical_data(symbol: str, to_date: str, timespan: str):
    client = StocksClient(
        api_key=API_KEY,
    )

    return_data = None
    most_recent_date = None
    is_not_enough_data = True

    while is_not_enough_data:
        if return_data == None:
            data = client.get_aggregate_bars(
            symbol= symbol,
            from_date= datetime.now().strftime("%Y-%m-%d"),
            to_date= to_date,
            timespan=timespan,
            limit= 60000,
            sort="desc"
            )

        # else:
        #     if 

def get_historical_to_csv(symbol):
    data = get_historical_data(symbol)
    print("here", data)
    df = pandas.DataFrame(data["results"])
    # df = pandas.DataFrame.to_datetime(df['t']).apply(lambda x: x.date())
    df['t'] = pandas.to_datetime(df["t"], unit='ms')
    print(df)
    df = df.drop(['vw', 'n'], axis=1)
    df.rename(columns = {'v':'volume', 'o':'open', 'c':'close', 'h':'high', 'l':'low', 't':'date'}, inplace = True)
    print(df)
    df.to_csv(f'Historical Data/{symbol}', mode="a")
    # json_data = df.to_dict()
    # print(json_data)
    # print(pandas.DataFrame(json_data))

if __name__=="__main__":
    # data = get_historical_data("GOOGL")
    # print(data["results"][-1]["t"])
    # date = datetime.fromtimestamp(int(data["results"][-1]["t"])/1000).strftime('%Y-%m-%d')
    # date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1656648000))
    
    # date_obj = datetime.strptime(date, '%Y-%m-%d')
    # print(date_obj)
    # df = pandas.DataFrame(data["results"])
    # df['t'] = pandas.to_datetime(df["t"], unit='ms')
    # df = df.drop(['vw', 'a','op', 'n'], axis=1)
    # df.rename(columns = {'v':'volume', 'o':'open', 'c':'close', 'h':'high', 'l':'low', 't':'date'}, inplace = True)
    # print(df)
    get_historical_to_csv("TSLA")