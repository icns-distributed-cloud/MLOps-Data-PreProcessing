from kafka import KafkaProducer

from app.internal.kafka.shared.custom_encoder import CustomJSONEncoder
from app.internal.kafka.shared.model_context import ScalingStrategy, Variable
from app.internal.kafka.shared.context_builder import ModelType, ModelContextBuilder

from app.internal.lstm import *

import torch
import json

def a():
    print(a)
# context build 하기


'''
Note:
- 프로그램을 builder instance가 돌아다니면서 채우던, 한 곳에서 몰아서 채우던 채워야함. 
- x_i는 최소 1개 이상. 
- 반드시 y와 동일한 x_i를 추가해야 함.
- 형식을 지키지 못한 context를 전달할 경우 예측 서버에서 context 갱신 이벤트를 무시
- hyperparameter는 각 모델의 __init__에서 요구하는 모든 파라미터를 dictionary로 명시해야한다. 그렇지 않을 경우 예측 서버에서 무시된다.
'''
def build_context(train_id, config, min_max_dict):
    print('build start')
    input_columns = config['input_columns']
    output_column = config['output_columns'][0]
    
    input_size = len(input_columns)
    hidden_size = config['hidden_size']
    
    if config['flag'] == 'mm':
        output_size = 12
    else:
        output_size = 1

    num_layers = config['num_layer']
    seq_len = config['seq_len']

    best_model_path = f'outputs/{train_id}/checkpoints/best.pkl'
    
    

    context_builder = ModelContextBuilder()

    for input_column in input_columns:
        index = input_column.rindex('_')
        input_id = input_column[index+1:]

        m, n = min_max_dict[input_column]['max'], min_max_dict[input_column]['min']

        x_ = Variable(variable_id=input_id, scaled=True, scaling_strategy=ScalingStrategy.MINMAX, min=n, max=m)
        context_builder.add_x_i(x_)
    
    index = output_column.rindex('_')
    output_id = output_column[index+1:]
    m, n = min_max_dict['output']['max'], min_max_dict['output']['min']
    
    y = Variable(variable_id=output_id, scaled=True, scaling_strategy=ScalingStrategy.MINMAX, min=n, max=m)
    context_builder.set_feature_id(output_id)
    context_builder.set_y(y)

    hyperparameter = {'input_size': input_size, 'hidden_size': hidden_size, 'output_size': output_size, 'num_layers': num_layers, 'seq_len': seq_len}
    context_builder.set_model_type(ModelType.LSTM)
    context_builder.set_model_hyperparameter(hyperparameter)
    
    model = LSTM(input_size=input_size, hidden_size=hidden_size, output_size=output_size, num_layers=num_layers)
    model.load_state_dict(torch.load(best_model_path)['models'])
    context_builder.set_model_state_dict(model.state_dict())

    context = context_builder.build()

    print('build done')
    return context


def publish_context(context, kafka_brokers, kafka_context_renewal_topic):
    print('publish start')
    try:
        producer = KafkaProducer(acks=1, bootstrap_servers=kafka_brokers, value_serializer=lambda x: json.dumps(x, cls=CustomJSONEncoder).encode('utf-8'))

        producer.send(kafka_context_renewal_topic, context)
        producer.flush()
        producer.close()

        return True
    
    except Exception as e:
        print(e)
        return False




'''
####### example #######
from {model_context 경로} import ScalingStrategy, Variable
from {context builder 경로} import ModelType, ModelContextBuilder
from  import ScalingStrategy, Variable
x_0 = Variable(variable_id="2", scaled=True, scaling_strategy=ScalingStrategy.MINMAX, min=3.0, max=5.0)
x_1 = Variable("2", False)
# x_2 = Variable("4", True, ScalingStrategy.No_SCALING) -> Exception(scaled but noscaling stategy)
# x_3 = Variable("5", True, ScalingStrategy.MINMAX) -> Exception(no given min, max values)

y = Variable("2", True, ScalingStrategy.MinMAX, 2.0, 7.0) # x_i중 하나의 feature_id와 동일해야 한다.

context_builder = ModelContextBuilder()
context_builder.set_feature_id("2")  # 어떤 feature를 위한 모델을 생성하는지
context_builder.add_x_i(x_0).add_x_i(x_1).set_y(y) # nested setting 쌉가능
# context = context_builder.build()  # 불충분한 field 설정 시 exception 발생
context_builder.set_model_type(ModelType.LSTM)
hyperparameter = {"input_size": 3, ~~~}  # model __init__에 있는 모든 파라미터
context_builder.set_model_hyperparameter(hyperparameter)
context_builder.set_model_state_dict(best_model.state_dict())

context = context_builder.build()
'''

# producer 설정하기
'''
# todo: 설정 받아오기(설정값 서버 활성화 후 통보)
kafka_brokers = ['']  # List[str]
context_renewal_event_topic = ""  # str

producer = KafkaProducer(acks=1, bootstrap_servers=kafka_brokers, value_serializer=lambda x: json.dumps(x, cls=CustomJSONEncoder).encode('utf-8'))
'''

# context publish 하기
'''
producer.send(context_renewal_event_topic, context)
producer.flush()
producer.close()
'''
