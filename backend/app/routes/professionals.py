from flask import Blueprint

bp = Blueprint("professionals", __name__)

@bp.route("/professionals")
def list_professionals():
    return "Lista de Profissionais"