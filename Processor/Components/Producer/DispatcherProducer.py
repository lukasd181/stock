from time import sleep
from json import dumps

from kafka import KafkaProducer


class DispatcherProducer():
    def __init__(self, ip_address, port, topic, key):
        self.key = key
        self.kafka_server = f"{ip_address}:{port}"
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers= [self.kafka_server],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )
 
    def send(self, data):
        self.producer.send(self.topic, value = data, key = self.key.encode())
        # sleep(5)
        self.producer.flush()