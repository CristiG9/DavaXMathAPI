from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db
from models import OperationModel
from schemas.operations import OperationSchema, OperationPublicSchema  # Pydantic
from pydantic import ValidationError

blp = Blueprint("Operation", "operation", description="Endpoints for operation definitions")

@blp.route("/operation")
class Operation(MethodView):
    def get(self):
        operations = OperationModel.query.all()
        return jsonify([
            OperationSchema.model_validate(op).model_dump() for op in operations
        ])

    @jwt_required()
    def post(self):
        try:
            data = OperationPublicSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        operation = OperationModel(
            name=data.name,
            description=data.description
        )

        try:
            db.session.add(operation)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Operation with this name already exists")
        except SQLAlchemyError:
            abort(500, message="Error while creating operation")

        return OperationSchema.model_validate(operation).model_dump(), 201

@blp.route("/operation/<string:op_name>")
class OperationInfo(MethodView):
    def get(self, op_name):
        operation = OperationModel.query.filter_by(name=op_name).first()
        if not operation:
            return {"message": "Operation not found"}, 404
        return OperationPublicSchema.model_validate(operation).model_dump(), 200

    @jwt_required()
    def delete(self, op_name):
        operation = OperationModel.query.filter_by(name=op_name).first()
        if not operation:
            return {"message": "Operation with this name not found"}, 404

        db.session.delete(operation)
        db.session.commit()
        return {"message": f"Operation '{op_name}' deleted successfully"}, 200
