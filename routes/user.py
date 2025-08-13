from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from pydantic import ValidationError
from schemas.user import UserRegisterSchema, UserLoginSchema  # Pydantic BaseModels
from models import UserModel
from db import db
from blocklist import BLOCKLIST

blp = Blueprint("User", "user", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    def post(self):
        try:
            data = UserRegisterSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        if UserModel.query.filter_by(username=data.username).first():
            abort(409, message="A user with that username already exists")

        if UserModel.query.filter_by(email=data.email).first():
            abort(409, message="A user with that email already exists")

        user = UserModel(
            username=data.username,
            email=data.email,
            password=pbkdf2_sha256.hash(data.password)
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

@blp.route("/user/<int:user_id>")
class User(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

@blp.route("/login")
class UserLogin(MethodView):
    def post(self):
        try:
            data = UserLoginSchema.model_validate_json(request.data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        user = UserModel.query.filter_by(username=data.username).first()
        if user and pbkdf2_sha256.verify(data.password, user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        abort(401, message="Invalid credentials")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Logged out successfully"}
