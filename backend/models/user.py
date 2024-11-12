# backend/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from config import mongo

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    @staticmethod
    def insert_user(user_data):
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})

    def check_password(self, password):
        return check_password_hash(self.password, password)
