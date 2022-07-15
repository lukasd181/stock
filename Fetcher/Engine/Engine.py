from threading import Thread
from polygon import StocksClient
from time import sleep
from datetime import datetime

class Engine(Thread):
    def __init__(self, symbol: str, 
                    api_key: str, 
                    kafka_producer,  
                    from_date: str = datetime.now().strftime("%Y-%m-%d"), 
                    to_date: str = datetime.now().strftime("%Y-%m-%d"), 
                    timespan: str = "minute", 
                    limit: int = 1):
        Thread.__init__(self)
        self.symbol = symbol
        self.api_key = api_key
        self.from_date = from_date
        self.to_date = to_date
        self.timespan =  timespan
        self.limit = limit
        self.kafka_producer = kafka_producer
    
    # def process_raw_data_to_csv(data, from_data: str, to_data :str):
        


    def run(self):
        client = StocksClient(self.api_key)
        print('Started Thread For: ' + self.symbol)
        while True:
            data = client.get_aggregate_bars(
                symbol=self.symbol,
                from_date=self.from_date,
                to_date=self.to_date,
                timespan=self.timespan,
                limit=self.limit,
                sort="desc"
            )
            data = data["results"]
            print(f"Data for {self.symbol}: {data}")
            if data:
                self.kafka_producer.send({"data": data})
                print("data sent")
            sleep(10)




