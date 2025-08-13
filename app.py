import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from db import db

from routes.user import blp as UserBlueprint
from routes.operation import blp as OperationBlueprint
from routes.operationLog import blp as OperationLogBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Math Buddy API "
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"]="3.1.0"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app,db)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "u6NccRkO8WZa5HQvWZ2AehZoXyGcJ6IckRfucNE9aFc"

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "Invalid token"}), 401

    @jwt.unauthorized_loader
    def unauthorized_token_callback(error):
        return jsonify({"message": "Unauthorized token", "error": "Authorization required"}), 401


    @app.before_request
    def create_tables():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(OperationBlueprint)
    api.register_blueprint(OperationLogBlueprint)

    return app