from flask import Flask
from app.database import init_db
from app.routes import gyms_bp, registrations_bp, payments_bp, search_bp
from app.routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gyms.db"

    # Inicializar o banco de dados
    init_db(app)

    # Registrar blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(gyms_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(search_bp)

    return app


