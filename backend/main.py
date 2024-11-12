import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))  # Certificando-se de que 'app' seja encontrado

from app import create_app, db  # Importa a função `create_app` e o banco de dados `db`
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify, request

# Inicialize o app
app = create_app()  # Chama a função `create_app` que vai configurar o Flask, o banco de dados, etc.

# Rota de Login (gera o token JWT)
@app.route('/api/login', methods=['POST'])
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
@app.route('/api/workouts/create', methods=['POST'])
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
@app.route('/api/workouts/<user_id>', methods=['GET'])
@jwt_required()
def get_workouts(user_id):
    current_user = get_jwt_identity()
    
    # Recupere a lista de treinos do banco de dados para o `user_id`
    # workouts = Workout.query.filter_by(user_id=user_id).all()
    workouts = [{"name": "Treino A", "duration": "30min"}]  # Exemplo de resposta

    return jsonify(workouts=workouts), 200

# Configuração para iniciar o aplicativo
if __name__ == '__main__':
    app.run(debug=True)



