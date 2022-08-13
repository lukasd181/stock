from threading import Thread
from Components.DispatcherStore import DispatcherStore
import pandas
from time import sleep
import threading
from threading import Thread
import concurrent.futures 

class Engine():
    def __init__(self, symbol, ip_address="localhost", port="29092"):
        self.symbol = symbol
        self.ip_address = ip_address
        self.port = port

        self.hist_data_model_portal = DispatcherStore.createModelProducer(
            key=f"hist_{self.symbol}", ip_address=self.ip_address, port=self.port
        )
        self.real_time_data_model_portal = DispatcherStore.createModelProducer(
            key=f"realtime_{self.symbol}", ip_address=self.ip_address, port=self.port
        )

        self.listening_data_from_hist_fetcher_thread = threading.Thread(
            target=self.create_historical_data_consumer, args=()
        )
        self.listening_data_from_hist_fetcher_thread.start()
        
        self.listening_data_from_realtime_fetcher_thread = threading.Thread(
            target = self.create_realtime_data_consumer, args=()
        )
        self.listening_data_from_realtime_fetcher_thread.start()
    
        self.run()
        
        

    def create_historical_data_consumer(self):
        raw_data_receiver = DispatcherStore.createHistoricalDataConsumer(
            key=self.symbol,
            callback=self.process_historical_data,
            ip_address=self.ip_address,
            port=self.port,
        )

    def process_historical_data(self, data):
        raw_data = data["data"]
        raw_df = pandas.DataFrame(raw_data)
        raw_df["t"] = pandas.to_datetime(raw_df["t"], unit="ms")
        raw_df = raw_df.drop(["vw", "n"], axis=1)
        raw_df.rename(
            columns={
                "v": "volume",
                "o": "open",
                "c": "close",
                "h": "high",
                "l": "low",
                "t": "date",
            },
            inplace=True,
        )

        json_data = raw_df.to_json(orient='records')
        self.hist_data_model_portal.send({"data": json_data, "id": data["id"]})
        print("data sent")
    
    def create_realtime_data_consumer(self):
        raw_realtime_data_receiver = DispatcherStore.createPolygonDataDispatcherConsumer(
            key=self.symbol,
            callback=self.process_realtime_data,
            ip_address=self.ip_address,
            port=self.port
        )
    
    def process_realtime_data(self,data):
        raw_data = data["data"]
        raw_df = pandas.DataFrame(raw_data)
        raw_df["t"] = pandas.to_datetime(raw_df["t"], unit="ms")
        raw_df = raw_df.drop(["vw", "n", "op", "a"], axis=1)
        raw_df.rename(
            columns={
                "v": "volume",
                "o": "open",
                "c": "close",
                "h": "high",
                "l": "low",
                "t": "date",
            },
            inplace=True,
        )
        json_data = raw_df.to_json(orient='records')
        self.real_time_data_model_portal.send({"data": json_data})

    def run(self):
        while True:
            sleep(5)
