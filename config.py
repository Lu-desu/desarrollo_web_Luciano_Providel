import os

class Config:
    SECRET_KEY = 'clave-secreta-para-tarea'
    SQLALCHEMY_DATABASE_URI = 'mysql://cc5002:programacionweb@localhost:3306/tarea2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload