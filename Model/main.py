from Engine.Engine import Engine
import concurrent.futures 
import pymongo as pm

if __name__ == "__main__":
 
  symbols = ["GOOGL", "AMZN", "NFLX", "AAPL", "META"]
  # symbols = ["GOOGL"]
  with concurrent.futures.ProcessPoolExecutor() as executor:
    
    engine = [executor.submit(Engine, symbol) for symbol in symbols]
