import asyncio
import json

from kafka import KafkaProducer

from utils import entry_factory

producer = KafkaProducer(
    bootstrap_servers=['localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


async def send_data():
    producer.send('posts', await entry_factory())
    producer.flush()
    print('Message sent!')


if __name__ == '__main__':
    asyncio.run(send_data())
