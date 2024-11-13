import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Definição da classe de configuração
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')  # Chave secreta do Flask
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///saas.db')  # URI do banco de dados SQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua_jwt_chave_secreta_aqui')  # Chave secreta para JWT

# Inicialização do aplicativo Flask com as configurações
app = Flask(_name_)
app.config.from_object(Config)

# Inicialização das extensões
db = SQLAlchemy(app)          # Para banco de dados relacional
jwt = JWTManager(app)         # Para autenticação JWT

# Modelos de Dados usando SQLAlchemy
class User(db.Model):
    _tablename_ = 'users'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    workouts = db.relationship('Workout', backref='user', lazy=True)

    def set_password(self, password):
        """Define o hash da senha do usuário."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

class Workout(db.Model):
    _tablename_ = 'workouts'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

# Rotas de Autenticação

@app.route('/api/register', methods=['POST'])
def register():
    """
    Rota para registrar um novo usuário.
    Espera um JSON com 'email' e 'password'.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(error="Email e senha são obrigatórios."), 400

    if User.query.filter_by(email=email).first():
        return jsonify(error="Usuário já registrado."), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Usuário registrado com sucesso."), 201

@app.route('/api/login', methods=['POST'])
def login():
    """
    Rota para login de usuário.
    Espera um JSON com 'email' e 'password'.
    Retorna um token JWT se as credenciais forem válidas.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify(error="Email e senha são obrigatórios."), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(token=access_token), 200
    return jsonify(error="Credenciais inválidas."), 401

# Rotas de Gerenciamento de Treinos

@app.route('/api/workouts/create', methods=['POST'])
@jwt_required()
def create_workout():
    """
    Rota para criar um novo treino.
    Requer autenticação JWT.
    Espera um JSON com 'name', 'duration' e 'date' (formato 'YYYY-MM-DD').
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    duration = data.get('duration')
    date_str = data.get('date')

    if not name or not duration or not date_str:
        return jsonify(error="Nome, duração e data são obrigatórios."), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify(error="Formato de data inválido. Use 'YYYY-MM-DD'."), 400

    workout = Workout(
        user_id=current_user_id,
        name=name,
        duration=duration,
        date=date
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify(message="Treino criado com sucesso.", workout={
        "id": workout.id,
        "name": workout.name,
        "duration": workout.duration,
        "date": workout.date.strftime('%Y-%m-%d')
    }), 201

@app.route('/api/workouts', methods=['GET'])
@jwt_required()
def list_workouts():
    """
    Rota para listar todos os treinos do usuário autenticado.
    Requer autenticação JWT.
    """
    current_user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=current_user_id).all()
    workouts_data = [
        {
            "id": workout.id,
            "name": workout.name,
            "duration": workout.duration,
            "date": workout.date.strftime('%Y-%m-%d')
        }
        for workout in workouts
    ]
    return jsonify(workouts=workouts_data), 200

@app.route('/api/workouts/<int:user_id>', methods=['GET'])
@jwt_required()
def get_workouts(user_id):
    """
    Rota para listar todos os treinos de um usuário específico.
    Requer autenticação JWT e que o usuário solicitado seja o próprio usuário autenticado.
    """
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify(error="Acesso negado."), 403

    workouts = Workout.query.filter_by(user_id=user_id).all()
    workouts_data = [
        {
            "id": workout.id,
            "name": workout.name,
            "duration": workout.duration,
            "date": workout.date.strftime('%Y-%m-%d')
        }
        for workout in workouts
    ]
    return jsonify(workouts=workouts_data), 200

# Inicialização do Banco de Dados
def initialize_database():
    if not os.path.exists('saas.db'):
        with app.app_context():
            db.create_all()
            print("Banco de dados criado.")

# Execução do Aplicativo
if _name_ == '_main_':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5001)




