from Components.DispatcherStore import DispatcherStore

producer = DispatcherStore.createHistoricalSignalProducer(key="GOOGL")
producer.send({"signal": "get_most_recent_historical_data", "symbol":"GOOGL"})
print("Signal Sent")