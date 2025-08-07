from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt,create_refresh_token,get_jwt_identity
from pyexpat.errors import messages
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from blocklist import BLOCKLIST
from db import db
from models import UserModel, OperationModel
from schemas import UserRegisterSchema, UserLogInSchema, OperationSchema,OperationPublicSchema

blp = Blueprint("Operations","operations")

@blp.route("/operation")
class Operation(MethodView):
    @blp.response(200,OperationSchema(many=True))
    def get(self):
        return OperationModel.query.all()

    @blp.arguments(OperationSchema)
    @blp.response(201,OperationSchema)
    @jwt_required()
    def post(self,operation_data):
        operation = OperationModel(**operation_data)
        try:
            db.session.add(operation)
            db.session.commit()
        except IntegrityError:
            abort(400,message = "Operation with this name already exists")
        except SQLAlchemyError:
            abort(500, message="Error when creating operation")
        return operation

@blp.route("/operation/<string:op_name>")
class OperationInfo(MethodView):
    @blp.response(200,OperationPublicSchema)
    def get(self, op_name):
        operation = OperationModel.query.filter_by(name = op_name).first()
        if operation:
            return operation
        return {"message": "Operation not found"}, 404

    @jwt_required()
    def delete(self, op_name):
        operation = OperationModel.query.filter_by(name = op_name).first()
        if operation:
            db.session.delete(operation)
            db.session.commit()
        else:
            return {"message" : "Operation with this name not found"},404
        return {"message":f"Operation {op_name} deleted succesfully"},200