from pydantic import BaseModel, Field

from app.models.response import *



class DataIn(BaseModel):
    """Use this data model to preprocessing the request data."""


    preDatasetMasterId: int = Field(..., example=9)
    path: str = Field(..., example="/home/icns/abc.csv")


class DataOut(BaseModel):
    """Use this data model to preprocessing the request data."""

    preDatasetMasterId: int = Field(..., example=9)
    path: str = Field(..., example="/home/icns/abc.csv")
