from datetime import datetime

from db import db

class OperationLogModel(db.Model):
    __tablename__ = "operationslogs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    operation_id = db.Column(db.Integer, db.ForeignKey("operations.id"), nullable=False)
    input_value = db.Column(db.String(100), nullable=False)
    output_value = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="logs")
    operation = db.relationship("OperationModel", back_populates="logs")