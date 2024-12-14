from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Gym

bp = Blueprint("gyms", __name__, url_prefix="/api/gyms")

# Listar todas as academias
@bp.route("/", methods=["GET"])
def list_gyms():
    gyms = Gym.query.all()
    return jsonify([{"id": gym.id, "name": gym.name, "address": gym.address} for gym in gyms])

# Adicionar uma nova academia
@bp.route("/", methods=["POST"])
def add_gym():
    data = request.get_json()
    new_gym = Gym(name=data["name"], address=data["address"])
    db.session.add(new_gym)
    db.session.commit()
    return jsonify({"message": "Academia adicionada com sucesso!"}), 201
