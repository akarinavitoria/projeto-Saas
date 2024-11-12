# backend/models/workout.py
from config import mongo

class Workout:
    def __init__(self, user_id, exercises, date):
        self.user_id = user_id
        self.exercises = exercises
        self.date = date

    @staticmethod
    def insert_workout(workout_data):
        return mongo.db.workouts.insert_one(workout_data)

    @staticmethod
    def find_by_user(user_id):
        return list(mongo.db.workouts.find({'user_id': user_id}))
