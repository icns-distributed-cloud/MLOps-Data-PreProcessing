from pydantic import BaseModel, Field


class ServingIn(BaseModel):
    """Use this data model to preprocessing the request data."""


    train_id: int = Field(..., example=1)

class ServingOut(BaseModel):
    """Use this data model to preprocessing the request data."""

    
    train_id: int = Field(..., example=1)



