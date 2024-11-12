from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicializando as extensões
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração do JWT
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'

    # Inicializando as extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Registrando rotas diretamente ou por meio de blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

