# consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'posts',
    bootstrap_servers=['localhost:9093'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

consumer.subscribe(['posts'])

while True:
    data = next(consumer)
    print(data.value)
    print(data)
