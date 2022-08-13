
from config import API_KEY
from polygon import StocksClient
from datetime import datetime
from Components.DispatcherStore import DispatcherStore
from time import sleep
import threading
from threading import Thread
import concurrent.futures as cf
import asyncio
import json

class Engine(Thread):
    def __init__(self, client, symbol, timespan: str="day", from_date: str="2016-01-01", to_date: str= datetime.now().strftime("%Y-%m-%d"), limit: int=50000, ip_address="localhost", port="29092"):
        Thread.__init__(self)
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.limit = limit
        self.timespan = timespan
        self.ip_address = ip_address
        self.port = port
        self.client = client
        self.signal_from_model_thread = threading.Thread(target=self.create_signal_listener, args=())
        self.signal_from_model_thread.start()
        
    def create_historical_data_producer(self, key):
        return DispatcherStore.createHistoricalDataProducer(key=key, ip_address=self.ip_address, port=self.port)

    def create_signal_listener(self):
        signal_listener = DispatcherStore.createHistoricalSignalConsumer(key=self.symbol,callback=self.signal_handler, ip_address=self.ip_address, port=self.port)
      
    
    def signal_handler(self, message):
        print(f"Message: {message}")
        if message["signal"] == "get_most_recent_historical_data":
            self.send_most_recent_historical_data(self.symbol, message["id"])
            
    def get_most_recent_historical_data(self, symbol):
        raw_data = None

        if self.symbol == "META":
            META_data = self.client.get_aggregate_bars(
                symbol="META",
                to_date=datetime.now().strftime("%Y-%m-%d"),
                from_date= "2022-06-09",
                sort="desc",
                timespan= self.timespan,
                limit=LIMIT
            )

            FB_data = self.client.get_aggregate_bars(
                symbol="FB",
                to_date="2022-06-08",
                from_date= self.from_date,
                sort="desc",
                timespan= self.timespan,
                limit=LIMIT
            )

            META_data['results'].extend(FB_data["results"])
            raw_data = META_data
        else:
            raw_data = self.client.get_aggregate_bars(
                symbol=symbol,
                to_date=datetime.now().strftime("%Y-%m-%d"),
                from_date=self.from_date,
                sort="desc",
                timespan=self.timespan,
                limit=self.limit
            )
        return raw_data

    def send_most_recent_historical_data(self, symbol, id):
        processor_portal = self.create_historical_data_producer(symbol)
        raw_data = self.get_most_recent_historical_data(symbol)["results"]
        processor_portal.send({"data": raw_data, "id": id})
        print(f"data sent for {self.symbol}.")

    def run(self):
        while True:
            sleep(5)