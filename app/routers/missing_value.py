from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator

from app.internal.utils import *
from app.internal.missing_value import *
from app.models.preprocessing import *
from app.models.response import *
from app.models.exceptions import *


import pandas as pd
import logging



log = logging.getLogger(__name__)
router = APIRouter()



@router.post('/preprocessing/missing-value/interpolate')
async def find_missing_value(item: PreprocessingIn, request: Request, background_tasks: BackgroundTasks, response_model=Response):
    origin_data_root_directory = request.app.config.origin_data_root_directory
    pre_data_root_directory = request.app.config.pre_data_root_directory
    
    origin_data_path = item.origin_data_path
    columns = item.colums
    db_id = item.db_id

    try: 
        origin_data = load_csv_data(f'{origin_data_root_directory}/{origin_data_path}')

        origin_columns = origin_data.columns
        valid_columns(columns, origin_columns)
        
        pre_data_path = f'{db_id}_{origin_data_path}'

        background_tasks.add_task(interpolate, origin_data, columns, pre_data_root_directory, pre_data_path)

        response = response_model(status=200, message="전처리 요청 성공", data=PreprocessingOut(origin_data_path=item.origin_data_path,
                                                                                            pre_data_path=pre_data_path,
                                                                                            colums=item.colums,
                                                                                            db_id=item.db_id))
        
    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response



@router.post('/preprocessing/missing-value/pearson')
async def find_missing_value(item: PreprocessingIn, request: Request, background_tasks: BackgroundTasks , response_model=Response):
    origin_data_root_directory = request.app.config.origin_data_root_directory
    pre_data_root_directory = request.app.config.pre_data_root_directory
    
    origin_data_path = item.origin_data_path  
    columns = item.colums
    db_id = item.db_id

    try:
        origin_data = load_csv_data(f'{origin_data_root_directory}/{origin_data_path}')

        origin_columns = origin_data.columns
        valid_columns(columns, origin_columns)
         
        pre_data_path = f'{db_id}_{origin_data_path}'
        background_tasks.add_task(pearson, origin_data, columns, pre_data_root_directory, pre_data_path)

        response = response_model(status=200, message="전처리 요청 성공", data=PreprocessingOut(origin_data_path=item.origin_data_path,
                                                                                            pre_data_path=pre_data_path,
                                                                                            colums=item.colums,
                                                                                            db_id=item.db_id))
        
    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response