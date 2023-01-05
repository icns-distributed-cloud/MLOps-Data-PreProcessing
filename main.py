import uvicorn

from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


from app.common.config import conf
from app.routers import missing_value
from app.models.response import *
from app.models.exceptions import *

def create_app():
    app = FastAPI(
        title='Icnslab MLOps data preprocessing',
        description='Data Preprocessing api for MLOps',
        version='0.1',
        docs_url='/docs'
    )

    

    # routers
    app.include_router(missing_value.router)
    app.config = conf()

    app.add_exception_handler(HTTPException, http_exception_handler)
    # app.add_exception_handler(APIException, exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']

    )


    return app






app = create_app()


if __name__ == '__main__':
    reload = app.config.project_reload


    uvicorn.run('main:app', host='0.0.0.0', port=8000, workers=3, reload=reload)