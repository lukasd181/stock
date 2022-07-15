from Components.DispatcherStore import DispatcherStore

def callback(data):
    print(data)

consumer = DispatcherStore.createPolygonDataDispatcherConsumer("AMZN", callback)
