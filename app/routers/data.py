from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator

from app.internal.utils import *
from app.internal.missing_value import *
from app.models.preprocessing import *
from app.models.data import *
from app.models.response import *
from app.models.exceptions import *


import pandas as pd
import logging



log = logging.getLogger(__name__)
router = APIRouter()



@router.post('/preprocessing/data/readpre')
async def find_missing_value(item: DataIn, request: Request, background_tasks: BackgroundTasks , response_model=Response):
    data_root_directory = request.app.config.data_root_directory
    
    preDatasetId = item.preDatasetId
    path = item.path

    file_path = f'{data_root_directory}{path}'
    

    try:
        mini_path = save_mini_data(file_path=file_path, source='origin', target='mini', db_id=preDatasetId, is_origin=True)
        response = response_model(status=200, message="미니 데이터셋 생성 완료", data=DataOut(preDatasetId=preDatasetId, path=mini_path))
        
    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response


@router.post('/preprocessing/transform')
async def transform_analysis(item: TransformationIn, request: Request, background_tasks: BackgroundTasks, response_model=Response):
    print('hello')
    data_root_directory = request.app.config.data_root_directory

    origin_data_path = item.origin_data_path
    pre_data_name = item.pre_data_name
    db_id = item.db_id

 
    try:
        origin_data = load_csv_data(f'{data_root_directory}/{origin_data_path}')
        
        background_tasks.add_task(transform_analysis_data, origin_data, f'datasets/pre/{pre_data_name}', db_id, f'{pre_data_name}')

        # mini_path = save_mini_data(file_path=file_path, source='origin', target='mini', db_id=preDatasetId, is_origin=True)
        # response = response_model(status=200, message="분석용 데이터셋 변환 완료", data=DataOut(preDatasetId=db_id, path=mini_path))
        response = response_model(status=200, message="분석용 데이터셋 변환 완료", data=DataOut(preDatasetId=db_id, path=f"datasets/pre/{pre_data_name}"))

    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response

