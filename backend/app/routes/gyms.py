from flask import Blueprint

bp = Blueprint("gyms", __name__)

@bp.route("/gyms")
def list_gyms():
    return "Lista de Academias"