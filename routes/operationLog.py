from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask_jwt_extended import  jwt_required,get_jwt_identity

from db import db
from models import UserModel, OperationModel, OperationLogModel
from schemas import  OperationLogSchema,FactorialInputSchema, OperationLogPublicSchema, PowInputSchema, FibonacciInputSchema
from services.math_logic import compute_factorial,compute_pow,compute_fibonacci

blp = Blueprint("OperationsLogs","operationsLogs")

@blp.route("/logs/me")
class LogsForUser(MethodView):
    @jwt_required()
    @blp.response(200, OperationLogPublicSchema(many=True))
    def get(self):
        id = get_jwt_identity()
        user = UserModel.query.get_or_404(id)

        if not user:
            return {"message": "User not found"}, 404

        logs = db.session.query(OperationLogModel).filter_by(user_id=id).all()

        simplified_logs = []
        for log in logs:
            simplified_logs.append({
                "username": user.username,
                "operation": log.operation.name,
                "input": log.input_value,
                "output": log.output_value,
                "timestamp":log.timestamp
            })

        return simplified_logs

@blp.route("/logs")
class AllLogs(MethodView):
    @jwt_required()
    @blp.response(200, OperationLogSchema(many=True))
    def get(self):
        return OperationLogModel.query.all()

@blp.route("/factorial")
class FactorialResource(MethodView):
    @jwt_required()
    @blp.arguments(FactorialInputSchema)
    @blp.response(200)
    def post(self, data):
        id = get_jwt_identity()
        user = UserModel.query.get_or_404(id)
        operation = OperationModel.query.filter_by(name="factorial").first()

        if not user:
            abort(404, message="User not found.")

        operation = OperationModel.query.filter_by(name="factorial").first()
        if not operation:
            abort(404, message="Operation 'factorial' not found.")

        n = data["n"]
        input_str = str(n)

        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        if cached:
            result = cached.output_value
        else:
            result = compute_factorial(n)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return {"result": float(result)}

@blp.route("/pow")
class PowResource(MethodView):
    @jwt_required()
    @blp.arguments(PowInputSchema)
    @blp.response(200)
    def post(self, data):
        id = get_jwt_identity()
        user = UserModel.query.get_or_404(id)
        if not user:
            abort(404, message="User not found.")

        operation = OperationModel.query.filter_by(name="pow").first()
        if not operation:
            abort(404, message="Operation 'pow' not found.")

        base = data["base"]
        exponent = data["exponent"]
        input_str = f"{base},{exponent}"

        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        if cached:
            result = cached.output_value
        else:
            result = compute_pow(base, exponent)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return {"result": float(result)}

@blp.route("/fibonacci")
class FibonacciResource(MethodView):
    @jwt_required()
    @blp.arguments(FibonacciInputSchema)
    @blp.response(200)
    def post(self, data):
        # Identificare utilizator
        id = get_jwt_identity()
        user = UserModel.query.get_or_404(id)
        if not user:
            abort(404, message="User not found.")

        operation = OperationModel.query.filter_by(name="fibonacci").first()
        if not operation:
            abort(404, message="Operation 'fibonacci' not found.")

        n = data["n"]
        input_str = str(n)

        cached = OperationLogModel.query.filter_by(
            operation_id=operation.id,
            input_value=input_str
        ).first()

        if cached:
            result = cached.output_value
        else:
            result = compute_fibonacci(n)

        log = OperationLogModel(
            user_id=user.id,
            operation_id=operation.id,
            input_value=input_str,
            output_value=str(result)
        )
        db.session.add(log)
        db.session.commit()

        return {"result": int(result)}
