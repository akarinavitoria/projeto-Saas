from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import db  # Importando o banco de dados

# Criando o Blueprint para as rotas
main_bp = Blueprint('main', __name__)

# Rota de Login (gera o token JWT)
@main_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Verifique as credenciais do usuário (exemplo de credenciais estáticas para teste)
    if email == 'user@example.com' and password == 'password':
        access_token = create_access_token(identity=email)
        return jsonify(token=access_token), 200
    else:
        return jsonify(error="Credenciais inválidas"), 401

# Rota para criar treino (exige autenticação JWT)
@main_bp.route('/api/workouts/create', methods=['POST'])
@jwt_required()
def create_workout():
    current_user = get_jwt_identity()  # Usuário autenticado
    workout_data = request.get_json()  # Dados do treino enviados pelo frontend
    
    # Salve o treino no banco de dados (exemplo simplificado)
    # workout = Workout(name=workout_data['name'], duration=workout_data['duration'], user_id=current_user)
    # db.session.add(workout)
    # db.session.commit()
    
    return jsonify(message="Treino criado com sucesso", workout=workout_data), 201

# Rota para listar treinos (exige autenticação JWT)
@main_bp.route('/api/workouts/<user_id>', methods=['GET'])
@jwt_required()
def get_workouts(user_id):
    current_user = get_jwt_identity()
    
    # Recupere a lista de treinos do banco de dados para o `user_id`
    # workouts = Workout.query.filter_by(user_id=user_id).all()
    workouts = [{"name": "Treino A", "duration": "30min"}]  # Exemplo de resposta

    return jsonify(workouts=workouts), 200
