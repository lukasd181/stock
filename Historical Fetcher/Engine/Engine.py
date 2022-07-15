from xml.etree.ElementTree import TreeBuilder
from config import API_KEY
from polygon import StocksClient
from datetime import datetime
from Components.DispatcherStore import DispatcherStore
from time import sleep
import threading

FROM_DATE = "2016-01-01"
LIMIT = 5000000

class Engine:
    def __init__(self, timespan: str="minute", ip_address="localhost", port="29092"):
        self.timespan = timespan
        self.ip_address = ip_address
        self.port = port
        self.client = StocksClient(
            api_key=API_KEY
        )
        self.signal_from_model_thread = threading.Thread(target=self.create_signal_listener, args=())
        self.signal_from_model_thread.start()
        
    def create_signal_listener(self):
        signal_listener = DispatcherStore.createHistoricalSignalConsumer(key="*",callback=self.signal_handler, ip_address=self.ip_address, port=self.port)

    
    def signal_handler(self, key, message):
        if message.value["signal"] == "get_most_recent_historical_data":
            raw_data = self.get_most_recent_historical_data(key)
            processor_portal = DispatcherStore.createProcessorProducer(key=key,ip_address=self.ip_address, port=self.port)
            processor_portal.send({"data": raw_data})

    def get_most_recent_historical_data(self, symbol):
        raw_data = self.client.get_aggregate_bars(
            symbol=symbol,
            to_date=datetime.now().strftime("%Y-%m-%d"),
            from_date= FROM_DATE,
            sort="desc",
            limit=LIMIT,
            full_range=True
        )
        return raw_data
   
    def run(self):
        while True:
            sleep(5)