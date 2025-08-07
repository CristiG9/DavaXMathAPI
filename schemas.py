from marshmallow import Schema,fields
from datetime import datetime

class UserRegisterSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required = True,load_only=True)

class UserLogInSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required=True)
    password = fields.Str(required = True,load_only=True)

class UserPublicSchema(Schema):
    id = fields.Int()
    username = fields.Str()

class OperationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class OperationPublicSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class OperationLogSchema(Schema):
    id = fields.Int(dump_only=True)

    user_id = fields.Int(required=True)
    operation_id = fields.Int(required=True)

    input_value = fields.Str(required=True)
    output_value = fields.Str()
    timestamp = fields.DateTime(required=True)

    user = fields.Nested(UserPublicSchema, dump_only=True)
    operation = fields.Nested(OperationSchema, dump_only=True)

class OperationLogPublicSchema(Schema):
    username = fields.Str()
    operation = fields.Str()
    input = fields.Str(required=True)
    output = fields.Str(required=True)
    timestamp = fields.DateTime(required=True)


class FactorialInputSchema(Schema):
    n = fields.Int(required=True, validate=lambda x: x >= 0)

class FibonacciInputSchema(Schema):
    n = fields.Int(required=True, validate=lambda x: x >= 0)

class PowInputSchema(Schema):
    base = fields.Float(required=True)
    exponent = fields.Float(required=True)