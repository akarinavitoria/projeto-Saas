from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Payment

bp = Blueprint("payments", __name__, url_prefix="/api/payments")

# Listar todos os pagamentos
@bp.route("/", methods=["GET"])
def list_payments():
    payments = Payment.query.all()
    return jsonify([{"id": pay.id, "user_id": pay.user_id, "amount": pay.amount, "status": pay.status} for pay in payments])

# Processar um novo pagamento
@bp.route("/", methods=["POST"])
def process_payment():
    data = request.get_json()
    new_payment = Payment(user_id=data["user_id"], amount=data["amount"], status="completed")
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Pagamento processado com sucesso!"}), 201
