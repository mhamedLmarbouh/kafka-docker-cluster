from abc import ABC, abstractmethod
import threading
import time
import unittest
from typing import Iterator
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

BOOTSTRAP_SERVER = 'localhost:9092'


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)

    def produce(self, topic, message):
        self.producer.send(topic, message)

    def close(self):
        self.producer.close()


class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVER,
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=1000)

    def consume(self, topic):
        self.consumer.subscribe([topic])
        for message in self.consumer:
            yield message

    def close(self):
        self.consumer.close()


def create_topic(topic_name):
    # Create 'my-topic' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVER)

        topic = NewTopic(name=topic_name,
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass


class TestKafkaCluster(unittest.TestCase):
    def setUp(self):
        self.TOPIC_NAME = 'my-topic'
        self.MESSAGES = [b'Message one', b'Message two']
        create_topic(self.TOPIC_NAME)
        self.producer = Producer()
        self.consumer = Consumer()

    def move_consumer_offset_to_last_index(self):
        for _ in self.consumer.consume(self.TOPIC_NAME):
            pass

    def test_kafka(self):
        self.move_consumer_offset_to_last_index()
        self.producer.produce(self.TOPIC_NAME, self.MESSAGES[0])
        self.producer.produce(self.TOPIC_NAME, self.MESSAGES[1])

        messages = []
        for message in self.consumer.consume(self.TOPIC_NAME):
            messages.append(message.value)

        self.assertListEqual(messages, self.MESSAGES)


if __name__ == '__main__':
    unittest.main()
