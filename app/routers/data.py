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


    # origin_data_root_directory = request.app.config.origin_data_root_directory
    pre_data_root_directory = request.app.config.pre_data_root_directory
    
 
    preDatasetId = item.preDatasetId
    path = item.path

    

    try:
        save_mini_data(f'{path}')
        response = response_model(status=200, message="미니 데이터셋 생성 완료", data=DataOut(preDatasetId=preDatasetId,
                                                                                            path=path))
        
    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response