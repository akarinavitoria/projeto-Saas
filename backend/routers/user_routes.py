# backend/routes/user_routes.py
from flask import Blueprint, request, jsonify
from models.user import User
from werkzeug.security import check_password_hash
import jwt
from config import Config
import datetime

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify({"error": "Usuário já registrado"}), 400

    user = User(data['name'], data['email'], data['password'], data['role'])
    User.insert_user(vars(user))
    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = User.find_by_email(data['email'])

    if user_data and check_password_hash(user_data['password'], data['password']):
        token = jwt.encode(
            {
                'user_id': str(user_data['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            Config.JWT_SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    return jsonify({"error": "Credenciais inválidas"}), 400
