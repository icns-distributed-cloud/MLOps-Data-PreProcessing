from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from typing import Union

from pydantic import BaseModel, Field





class Response(BaseModel):
    """Use this data model to preprocessing the request data."""

    status: int = Field(..., example=200)
    message: str = Field(..., example="성공")
    data: Union[BaseModel, None] = Field()



async def http_exception_handler(request: Request, exec: HTTPException):
    print(exec)
    return JSONResponse(
        status_code=400,
        content={"message": "good"}
    )