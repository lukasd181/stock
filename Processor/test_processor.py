from Components.DispatcherStore import DispatcherStore
import pandas as pd

def callback(data):
    print(type(data))
    df = pd.DataFrame(data["data"])
    print(df)

model_receiver = DispatcherStore.createModelConsumer(key="hist_GOOGL",callback=callback)

