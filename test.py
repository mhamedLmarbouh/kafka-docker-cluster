from abc import ABC, abstractmethod
import threading
import time
import unittest
from typing import Iterator
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic


class Producer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def produce(self, topic, message):
        self.producer.send(topic, message)

    def close(self):
        self.producer.close()


class Consumer:
    def __init__(self, bootstrap_servers):
        self.consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=1000)

    def consume(self, topic):
        self.consumer.subscribe([topic])
        for message in self.consumer:
            yield message

    def close(self):
        self.consumer.close()


class Admin:
    def __init__(self, bootstrap_servers):
        self.admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic):
        try:
            topic = NewTopic(name=topic,
                            num_partitions=1,
                            replication_factor=1)
            self.admin.create_topics([topic], timeout_ms=2000)
        except Exception:
            pass

    def delete_topic(self, topic):
        res = self.admin.delete_topics([topic], 2000)
        print(res)
    
    def close(self):
        self.admin.close()

class TestKafkaCluster(unittest.TestCase):
    BOOTSTRAP_SERVER = 'localhost:9091,localhost:9092,localhost:9093'
    TOPIC_NAME = 'test-topic'
    MESSAGES = [b'test one', b'test two']

    def setUp(self): 
        self.admin = Admin(self.BOOTSTRAP_SERVER)
        self.producer = Producer(self.BOOTSTRAP_SERVER)
        self.consumer = Consumer(self.BOOTSTRAP_SERVER)

        self.admin.create_topic(self.TOPIC_NAME)
    
    def tearDown(self):
        self.admin.delete_topic(self.TOPIC_NAME)
        self.admin.close()
        self.producer.close()
        self.consumer.close()

    def test_kafka(self):
        self.producer.produce(self.TOPIC_NAME, self.MESSAGES[0])
        self.producer.produce(self.TOPIC_NAME, self.MESSAGES[1])

        messages = []
        for message in self.consumer.consume(self.TOPIC_NAME):
            messages.append(message.value)

        self.assertListEqual(messages, self.MESSAGES)


if __name__ == '__main__':
    unittest.main()
