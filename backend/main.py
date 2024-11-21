from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta_segura"
jwt = JWTManager(app)

# Ativando o CORS para permitir conexões do frontend
CORS(app)

# Armazenamento temporário de clientes e treinos (simulando um banco de dados)
clients = []
workouts = [
    {
        "id": 1,
        "name": "Treino de Peito",
        "duration": 60,
        "date": "2024-11-20"
    },
    {
        "id": 2,
        "name": "Treino de Pernas",
        "duration": 45,
        "date": "2024-11-19"
    },
    {
        "id": 3,
        "name": "Treino de Costas",
        "duration": 50,
        "date": "2024-11-18"
    }
]

users = [
    {"id": 1, "username": "admin", "password": "admin123"}  # Usuário fictício
]

# Função auxiliar para validar os dados de treino
def validate_workout(data):
    required_fields = ["name", "duration", "date"]
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"O campo '{field}' é obrigatório.")
    if "duration" in data and not isinstance(data["duration"], int):
        errors.append("O campo 'duration' deve ser um número inteiro representando minutos.")
    if "date" in data:
        try:
            year, month, day = map(int, data["date"].split("-"))
        except ValueError:
            errors.append("O campo 'date' deve estar no formato YYYY-MM-DD.")
    return errors

# Rotas de autenticação
@app.route('/api/login', methods=['POST'])
def login():
    credentials = request.json
    user = next((u for u in users if u["username"] == credentials.get("username") and u["password"] == credentials.get("password")), None)
    if not user:
        return jsonify({"error": "Credenciais inválidas."}), 401
    access_token = create_access_token(identity=user["id"])
    return jsonify({"access_token": access_token}), 200

# Rotas de clientes
@app.route('/api/clients', methods=['POST'])
@jwt_required()
def add_client():
    try:
        new_client = request.json
        if not new_client.get("name") or not new_client.get("email"):
            return jsonify({"error": "Os campos 'name' e 'email' são obrigatórios."}), 400
        new_client["id"] = len(clients) + 1
        clients.append(new_client)
        return jsonify(new_client), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao adicionar cliente: {str(e)}"}), 500

# Rotas de treinos
@app.route('/api/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    return jsonify(workouts), 200

@app.route('/api/workouts', methods=['POST'])
@jwt_required()
def add_workout():
    try:
        new_workout = request.json
        errors = validate_workout(new_workout)
        if errors:
            return jsonify({"errors": errors}), 400
        new_workout["id"] = len(workouts) + 1
        workouts.append(new_workout)
        return jsonify(new_workout), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao adicionar treino: {str(e)}"}), 500

@app.route('/api/workouts/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout_by_id(workout_id):
    workout = next((w for w in workouts if w["id"] == workout_id), None)
    if workout:
        return jsonify(workout), 200
    return jsonify({"error": "Treino não encontrado."}), 404

@app.route('/api/workouts/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    global workouts
    workout_to_delete = next((w for w in workouts if w["id"] == workout_id), None)
    if not workout_to_delete:
        return jsonify({"error": "Treino não encontrado."}), 404
    workouts = [w for w in workouts if w["id"] != workout_id]
    return jsonify({"message": "Treino removido com sucesso."}), 200

@app.route('/api/workouts/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    try:
        updated_data = request.json
        workout = next((w for w in workouts if w["id"] == workout_id), None)
        if not workout:
            return jsonify({"error": "Treino não encontrado."}), 404
        errors = validate_workout(updated_data)
        if errors:
            return jsonify({"errors": errors}), 400
        workout.update(updated_data)
        return jsonify(workout), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar treino: {str(e)}"}), 500

# Rota inicial
@app.route('/')
def home():
    return jsonify({"message": "API do Gym Manager está rodando!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
