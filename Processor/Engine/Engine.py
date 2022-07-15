from threading import Thread
from Components.DispatcherStore import DispatcherStore
import pandas
from time import sleep
import threading
class Engine():
    def __init__(self, symbol, ip_address="localhost", port="29092"):
        self.symbol = symbol
        self.ip_address = ip_address
        self.port = port
        self.hist_data_model_portal = DispatcherStore.createModelProducer(key=f'hist_{self.symbol}',ip_address=self.ip_address, port=self.port)
        self.real_time_data_model_portal = DispatcherStore.createModelProducer(key=f'realtime_{self.symbol}',ip_address=self.ip_address, port=self.port)
        self.listening_data_from_hist_fetcher_thread = threading.Thread(target=self.create_historical_data_consumer, args=())
        self.listening_data_from_hist_fetcher_thread.start()

    def create_historical_data_consumer(self):
        raw_data_receiver = DispatcherStore.createProcessorConsumer(key=self.symbol, callback=self.process_historical_data, ip_address=self.ip_address, port=self.port)

    def process_historical_data(self, data):
        raw_data = data["data"]
        raw_df = pandas.DataFrame(raw_data)
        raw_df['t'] = pandas.to_datetime(raw_df["t"], unit='ms')
        raw_df = raw_df.drop(['vw', 'n'], axis=1)
        raw_df.rename(columns = {'v':'volume', 'o':'open', 'c':'close', 'h':'high', 'l':'low', 't':'date'}, inplace = True)
        self.hist_data_model_portal.send({"data": raw_df.to_dict()})
        print("data sent")

    def run(self):
        while True:
            sleep(5)
        
