from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class FactorialInputSchema(BaseModel):
    n: conint(ge=0)

class FibonacciInputSchema(BaseModel):
    n: conint(ge=0)

class PowInputSchema(BaseModel):
    base: float
    exponent: float
