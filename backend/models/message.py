# backend/models/message.py
from config import mongo

class Message:
    def __init__(self, sender_id, receiver_id, content, timestamp):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = timestamp

    @staticmethod
    def insert_message(message_data):
        return mongo.db.messages.insert_one(message_data)

    @staticmethod
    def get_conversation(user1_id, user2_id):
        return list(mongo.db.messages.find({
            '$or': [
                {'sender_id': user1_id, 'receiver_id': user2_id},
                {'sender_id': user2_id, 'receiver_id': user1_id}
            ]
        }))
