from Engine.Engine import Engine
from config import API_KEY
from polygon import StocksClient

polygon_client = StocksClient(api_key=API_KEY)
symbols = ["GOOGL", "AMZN", "NFLX", "AAPL", "META"]
if __name__ == "__main__":
    for symbol in symbols:
        print("Start Hist Fetcher For ", symbol)
        engine = Engine(polygon_client, symbol)
        engine.start()
