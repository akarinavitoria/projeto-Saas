from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Registration

bp = Blueprint("registrations", __name__, url_prefix="/api/registrations")

# Listar todas as inscrições
@bp.route("/", methods=["GET"])
def list_registrations():
    registrations = Registration.query.all()
    return jsonify([{"id": reg.id, "user_id": reg.user_id, "gym_id": reg.gym_id, "plan": reg.plan} for reg in registrations])

# Criar uma nova inscrição
@bp.route("/", methods=["POST"])
def create_registration():
    data = request.get_json()
    new_registration = Registration(user_id=data["user_id"], gym_id=data["gym_id"], plan=data["plan"])
    db.session.add(new_registration)
    db.session.commit()
    return jsonify({"message": "Inscrição criada com sucesso!"}), 201

