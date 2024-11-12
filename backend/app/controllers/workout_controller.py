from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_model import Workout, User
from app import db

workout_bp = Blueprint('workout', __name__)

@workout_bp.route('/api/workouts/create', methods=['POST'])
@jwt_required()
def create_workout():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    workout = Workout(
        user_id=current_user_id,
        name=data.get('name'),
        duration=data.get('duration'),
        date=data.get('date')
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify(message="Treino criado com sucesso."), 201

@workout_bp.route('/api/workouts', methods=['GET'])
@jwt_required()
def list_workouts():
    current_user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=current_user_id).all()
    workouts_data = [
        {"name": workout.name, "duration": workout.duration, "date": workout.date.strftime('%Y-%m-%d')}
        for workout in workouts
    ]
    return jsonify(workouts=workouts_data), 200
