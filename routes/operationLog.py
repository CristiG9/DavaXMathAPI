from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from db import db
from models import UserModel, OperationModel, OperationLogModel
from schemas.operation_log import OperationLogPublicSchema
from schemas.input import FactorialInputSchema, FibonacciInputSchema, PowInputSchema
from services.math_logic import compute_factorial, compute_pow, compute_fibonacci

blp = Blueprint("Operation_log", "operation_log", description="Endpoints for operation definitions")


@blp.route("/logs/me")
class LogsForUser(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)

        logs = OperationLogModel.query.filter_by(user_id=user.id).all()

        return jsonify([
            OperationLogPublicSchema(
                username=user.username,
                operation=log.operation.name,
                input=log.input_value,
                output=log.output_value,
                timestamp=log.timestamp
            ).model_dump()
            for log in logs
        ])

@blp.route("/logs")
class AllLogs(MethodView):
    @jwt_required()
    def get(self):
        logs = OperationLogModel.query.all()
        return jsonify([
            {
                "user_id": log.user_id,
                "operation": log.operation.name,
                "input": log.input_value,
                "output": log.output_value,
                "timestamp": log.timestamp
            }
            for log in logs
        ])

@blp.route("/factorial")
class FactorialResource(MethodView):
    @jwt_required()
    def post(self):
        try:
            data = FactorialInputSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        user = UserModel.query.get_or_404(get_jwt_identity())
        operation = OperationModel.query.filter_by(name="factorial").first()
        if not operation:
            abort(404, message="Operation 'factorial' not found.")

        input_str = str(data.n)
        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        result = cached.output_value if cached else compute_factorial(data.n)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"result": float(result)})

@blp.route("/pow")
class PowResource(MethodView):
    @jwt_required()
    def post(self):
        try:
            data = PowInputSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        user = UserModel.query.get_or_404(get_jwt_identity())
        operation = OperationModel.query.filter_by(name="pow").first()
        if not operation:
            abort(404, message="Operation 'pow' not found.")

        input_str = f"{data.base},{data.exponent}"
        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        result = cached.output_value if cached else compute_pow(data.base, data.exponent)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"result": float(result)})

@blp.route("/fibonacci")
class FibonacciResource(MethodView):
    @jwt_required()
    def post(self):
        try:
            data = FibonacciInputSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        user = UserModel.query.get_or_404(get_jwt_identity())
        operation = OperationModel.query.filter_by(name="fibonacci").first()
        if not operation:
            abort(404, message="Operation 'fibonacci' not found.")

        input_str = str(data.n)
        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        result = cached.output_value if cached else compute_fibonacci(data.n)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({"result": int(result)})
