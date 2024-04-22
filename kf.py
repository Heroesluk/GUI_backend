# producer.py
import json

from kafka import KafkaProducer

from utils import getRecord

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    producer.send('posts', str(getRecord()))
    producer.flush()
    print('Message sent!')