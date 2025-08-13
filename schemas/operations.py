from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class OperationSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class OperationPublicSchema(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True

