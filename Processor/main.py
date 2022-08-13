from Engine.Engine import Engine
import concurrent.futures

if __name__ == "__main__":
    symbols = ["GOOGL", "AMZN", "NFLX", "AAPL", "META"]
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(symbols)) as executor:
        engine = [executor.submit(Engine, symbol) for symbol in symbols]
        