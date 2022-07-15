from sys import api_version
from kafka.admin import KafkaAdminClient, NewTopic
class TopicCreator():
    @staticmethod
    def create_topic(topic_name, ip_address="localhost", port="9092"):
        print("here1")
        admin_client = KafkaAdminClient(
            api_version=(0, 9),
            bootstrap_servers=f"{ip_address}:{port}", 
            client_id='stock'
        )
       
        topic_list = []
        topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

TopicCreator.create_topic("Polygon")