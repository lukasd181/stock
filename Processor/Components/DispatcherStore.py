from Components.Producer.DispatcherProducer import DispatcherProducer
from Components.Consumer.DispatcherConsumer import DispatcherConsumer

class DispatcherStore:
    IP_ADDRESS="localhost"
    PORT="29092"
    
    @staticmethod
    def createPolygonDataDispatcherProducer(key: str, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherProducer(ip_address=ip_address, port=port, topic="Polygon", key=key)

    @staticmethod
    def createPolygonDataDispatcherConsumer(key: str, callback, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherConsumer(ip_address=ip_address, port=port, topic="Polygon", key=key, callback=callback)

    @staticmethod
    def createHistoricalSignalProducer(key: str, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherProducer(ip_address=ip_address, port=port, topic="HistoricalSignal", key=key)

    @staticmethod
    def createHistoricalSignalConsumer(key: str, callback, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherConsumer(ip_address=ip_address, port=port, topic="HistoricalSignal", key=key, callback=callback)

    @staticmethod
    def createProcessorProducer(key: str, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherProducer(ip_address=ip_address, port=port, topic="Processor", key=key)

    @staticmethod
    def createProcessorConsumer(key: str, callback, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherConsumer(ip_address=ip_address, port=port, topic="Processor", key=key, callback=callback)

    @staticmethod
    def createModelProducer(key: str, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherProducer(ip_address=ip_address, port=port, topic="Model", key=key)

    @staticmethod
    def createModelConsumer(key: str, callback, ip_address=IP_ADDRESS, port=PORT):
        return DispatcherConsumer(ip_address=ip_address, port=port, topic="Model", key=key, callback=callback)

    