from fastapi import BackgroundTasks

from app.internal.kafka.producer import *

import json

def load_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config



def serve_trained_model(train_id, kafka_brokers, kafka_context_renewal_topic):
    config = load_config(f'outputs/{train_id}/config.json')
    min_max_dict = load_config(f'outputs/{train_id}/min_max.json')

    context = build_context(train_id, config, min_max_dict)

    publish_context(context, kafka_brokers, kafka_context_renewal_topic)


    print('publish done!!!!!!!')









