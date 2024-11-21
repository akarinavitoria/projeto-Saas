from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Ativando o CORS para permitir conexões do frontend
CORS(app)

# Dados fictícios para treinos (substituir por um banco de dados no futuro)
workouts = [
    {
        "id": 1,
        "name": "Treino de Peito",
        "duration": 60,  # Duração em minutos
        "date": "2024-11-20"  # Data no formato YYYY-MM-DD
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

# Função auxiliar para validar os dados de um treino
def validate_workout(data):
    required_fields = ["name", "duration", "date"]
    errors = []

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"O campo '{field}' é obrigatório.")
    
    if "duration" in data and not isinstance(data["duration"], int):
        errors.append("O campo 'duration' deve ser um número inteiro representando minutos.")
    
    # Valida o formato da data (simplificado)
    if "date" in data:
        try:
            year, month, day = map(int, data["date"].split("-"))
        except ValueError:
            errors.append("O campo 'date' deve estar no formato YYYY-MM-DD.")
    
    return errors

# Rota para listar todos os treinos
@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    return jsonify(workouts), 200

# Rota para adicionar um novo treino
@app.route('/api/workouts', methods=['POST'])
def add_workout():
    try:
        new_workout = request.json
        errors = validate_workout(new_workout)

        if errors:
            return jsonify({"errors": errors}), 400

        # Cria um novo ID automaticamente
        new_workout["id"] = len(workouts) + 1
        workouts.append(new_workout)
        return jsonify(new_workout), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao adicionar treino: {str(e)}"}), 500

# Rota para obter um treino específico pelo ID
@app.route('/api/workouts/<int:workout_id>', methods=['GET'])
def get_workout_by_id(workout_id):
    workout = next((w for w in workouts if w["id"] == workout_id), None)
    if workout:
        return jsonify(workout), 200
    return jsonify({"error": "Treino não encontrado."}), 404

# Rota para deletar um treino pelo ID
@app.route('/api/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    global workouts
    workout_to_delete = next((w for w in workouts if w["id"] == workout_id), None)
    if not workout_to_delete:
        return jsonify({"error": "Treino não encontrado."}), 404
    
    workouts = [w for w in workouts if w["id"] != workout_id]
    return jsonify({"message": "Treino removido com sucesso."}), 200

# Rota para atualizar um treino pelo ID
@app.route('/api/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    try:
        updated_data = request.json
        workout = next((w for w in workouts if w["id"] == workout_id), None)
        if not workout:
            return jsonify({"error": "Treino não encontrado."}), 404

        # Valida os dados atualizados
        errors = validate_workout(updated_data)
        if errors:
            return jsonify({"errors": errors}), 400

        # Atualiza apenas os campos fornecidos
        workout.update(updated_data)
        return jsonify(workout), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar treino: {str(e)}"}), 500

# Rota inicial para verificar se o servidor está rodando
@app.route('/')
def home():
    return jsonify({"message": "API do Gym Manager está rodando!"}), 200

if __name__ == '__main__':
    # Use debug=True apenas em desenvolvimento. Em produção, use um servidor WSGI.
    app.run(host='0.0.0.0', port=5000, debug=True)









