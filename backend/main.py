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

# Configuração do aplicativo
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///saas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua_jwt_chave_secreta_aqui')

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Classe User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    workouts = db.relationship('Workout', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Classe Workout
class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

# Rota: Registro de Usuário
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios.'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Usuário já cadastrado.'}), 400

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota: Login de Usuário
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios.'}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas.'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota: Criar Treino
@app.route('/api/workouts/create', methods=['POST'])
@jwt_required()
def create_workout():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        name = data.get('name')
        duration = data.get('duration')
        date = data.get('date')

        if not name or not duration or not date:
            return jsonify({'error': 'Nome, duração e data são obrigatórios.'}), 400

        new_workout = Workout(
            user_id=current_user_id,
            name=name,
            duration=duration,
            date=datetime.strptime(date, '%Y-%m-%d')
        )

        db.session.add(new_workout)
        db.session.commit()

        return jsonify({'message': 'Treino criado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota: Listar Treinos
@app.route('/api/workouts', methods=['GET'])
@jwt_required()
def list_workouts():
    try:
        current_user_id = get_jwt_identity()
        workouts = Workout.query.filter_by(user_id=current_user_id).all()

        workout_list = [
            {
                'id': workout.id,
                'name': workout.name,
                'duration': workout.duration,
                'date': workout.date.strftime('%Y-%m-%d')
            }
            for workout in workouts
        ]

        return jsonify(workout_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inicializar banco de dados
def initialize_database():
    if not os.path.exists('saas.db'):
        with app.app_context():
            db.create_all()
            print("Banco de dados criado.")

# Inicialização
if __name__ == '__main__':
    print("Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule}")
    initialize_database()
    app.run(debug=True)







