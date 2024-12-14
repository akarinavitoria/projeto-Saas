from flask import Flask
from .database import init_db
from .routes import clients, gyms, professionals

def create_app():
    app = Flask(__name__)
    init_db(app)

    # Registrar Blueprints para as rotas
    app.register_blueprint(clients.bp)
    app.register_blueprint(gyms.bp)
    app.register_blueprint(professionals.bp)

    return app

