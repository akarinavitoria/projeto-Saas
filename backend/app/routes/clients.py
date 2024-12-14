from flask import Blueprint

bp = Blueprint("clients", __name__)

@bp.route("/clients")
def list_clients():
    return "Lista de clientes"
