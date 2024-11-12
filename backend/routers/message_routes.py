# backend/routes/message_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import Message
import datetime

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender_id = get_jwt_identity()  # Usuário autenticado como remetente

    message = Message(
        sender_id=sender_id,
        receiver_id=data['receiver_id'],
        content=data['content'],
        timestamp=datetime.datetime.utcnow()
    )
    message_id = Message.insert_message(vars(message)).inserted_id
    
    return jsonify({"message": "Mensagem enviada com sucesso", "message_id": str(message_id)}), 201

@message_bp.route('/conversation/<user_id>', methods=['GET'])
@jwt_required()
def get_conversation(user_id):
    # Usuário autenticado visualiza a conversa com outro usuário
    current_user_id = get_jwt_identity()
    messages = Message.get_conversation(current_user_id, user_id)
    
    return jsonify({"messages": messages}), 200
