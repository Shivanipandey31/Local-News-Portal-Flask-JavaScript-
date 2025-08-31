from flask import Blueprint, request, jsonify
from news_fetcher import fetch_and_store_news
from models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token 

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "error": "Username & password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

    fetch_and_store_news(country="in") 

    token = create_access_token(identity=str(user.id))

    return jsonify({"success": True, "access_token": token, "message": f"Welcome {username}!"}), 200
