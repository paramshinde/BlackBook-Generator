import os

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token

from ..extensions import db
from ..models.user import User

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    payload = request.get_json() or {}
    email = payload.get("email", "student@blackbook.local").lower().strip()
    password = payload.get("password", "blackbook123")
    name = payload.get("name", "Default Student")

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, role="student")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    if not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"access_token": token, "user": {"id": user.id, "name": user.name, "email": user.email}})
