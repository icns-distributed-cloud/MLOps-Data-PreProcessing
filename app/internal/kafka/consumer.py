from kafka import KafkaConsumer, TopicPartition
import json
from shared.custom_decoder import CustomJSONDecoder

# todo: 설정 받아오기(설정값 서버 활성화 후 통보)
kafka_brokers = ['']  # List[str]
context_renewal_event_topic = ""  # str

consumer = KafkaConsumer(bootstrap_servers=kafka_brokers, value_deserializer=lambda m: json.loads(m.decode('utf-8'), cls=CustomJSONDecoder))
tp = TopicPartition(context_renewal_event_topic, 0)
consumer.assign([tp])

for message in consumer:
    context = message.value
