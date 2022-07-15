import polygon
from config import API_KEY
from polygon import StocksClient
from Engine.Engine import Engine
from datetime import datetime
from Components.DispatcherStore import DispatcherStore
from datetime import datetime

symbols = ["AMZN"]
if __name__=="__main__":
    for symbol in symbols:
        producer = DispatcherStore.createPolygonDataDispatcherProducer(symbol)
        engine = Engine(
            symbol,
            API_KEY,
            producer,
        )
        engine.start()

# stocks_client = polygon.StocksClient(API_KEY)
# with polygon.StocksClient(API_KEY) as client:
#     last_quote = client.get_aggregate_bars('AMD',from_date='2022-06-23', to_date='2022-06-23', timespan='minute', limit=1, sort="desc")
#     print(f'Last quote for AMD: {last_quote}')