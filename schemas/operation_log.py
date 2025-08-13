from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class OperationLogSchema(BaseModel):
    id: int
    user_id: int
    operation_id: int
    input_value: str
    output_value: str
    timestamp: datetime

class OperationLogPublicSchema(BaseModel):
    username: str
    operation: str
    input: str
    output: str
    timestamp: datetime
