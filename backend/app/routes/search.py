from flask import Blueprint, jsonify, request
from app.models import Gym

bp = Blueprint("search", __name__, url_prefix="/api/search")

# Buscar academias por proximidade (simulado)
@bp.route("/", methods=["GET"])
def search_gyms():
    location = request.args.get("location")
    # Simulação de uma busca de academias próximas
    gyms = Gym.query.all()
    return jsonify([{"id": gym.id, "name": gym.name, "address": gym.address} for gym in gyms])
