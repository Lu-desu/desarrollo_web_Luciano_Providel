import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, upload_folder):
    """Guarda un archivo con nombre único y devuelve su nombre"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generar nombre único para evitar colisiones
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def format_datetime(date_str):
    """Convierte un string de fecha/hora a objeto datetime"""
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        return None
