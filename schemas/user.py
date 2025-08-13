from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserPublicSchema(BaseModel):
    id: int
    username: str
