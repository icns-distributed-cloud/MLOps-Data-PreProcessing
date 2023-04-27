from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator

from app.internal.serving import *

from app.models.serving import *
from app.models.response import *
from app.models.exceptions import *

import logging



log = logging.getLogger(__name__)
router = APIRouter()


@router.post('/model/serving')
async def serve_model(item: ServingIn, request: Request, background_tasks: BackgroundTasks, response_model=Response):
    kafka_brokers = request.app.config.kafka_brokers
    kafka_context_renewal_topic = request.app.config.kafka_context_renewal_topic

    
    train_id = item.train_id

    try:
        background_tasks.add_task(serve_trained_model, train_id, kafka_brokers, kafka_context_renewal_topic)

        response = response_model(status=200, message="모델 서빙 요청 성공", data=ServingOut(train_id=train_id))



    except Exception as e:
        print(e)
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, message=error.message, data=None)
        response = JSONResponse(status_code=error.status_code, content=error_dict)

    return response





