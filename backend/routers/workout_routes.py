# backend/routes/workout_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.workout import Workout
import datetime

workout_bp = Blueprint('workout_bp', __name__)

@workout_bp.route('/create', methods=['POST'])
@jwt_required()
def create_workout():
    data = request.get_json()
    user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    
    workout = Workout(
        user_id=user_id,
        exercises=data['exercises'],
        date=datetime.datetime.utcnow()
    )
    workout_id = Workout.insert_workout(vars(workout)).inserted_id
    
    return jsonify({"message": "Treino criado com sucesso", "workout_id": str(workout_id)}), 201

@workout_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_workouts(user_id):
    # Listar treinos por usuário autenticado
    workouts = Workout.find_by_user(user_id)
    return jsonify({"workouts": workouts}), 200
