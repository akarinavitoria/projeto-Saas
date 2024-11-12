# backend/config.py
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
