from flask import Blueprint
from .gyms import bp as gyms_bp
from .registrations import bp as registrations_bp
from .payments import bp as payments_bp
from .search import bp as search_bp

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return {"message": "Bem-vindo ao sistema de avaliação de academias!"}

__all__ = ["gyms_bp", "registrations_bp", "payments_bp", "search_bp"]
