from db import db

class OperationModel(db.Model):
    __tablename__ = "operations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100),nullable = False)

    logs = db.relationship("OperationLogModel", back_populates="operation", cascade="all, delete-orphan")