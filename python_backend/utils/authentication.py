# utils/authentication.py
from flask import session,request, jsonify
from functools import wraps
from models import User
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()

def authenticate_user(name, surname, password):
    # Query by combining name and surname
    user = User.query.filter_by(name=name, surname=surname).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        start_session(user.id)
    else:
        return None

def start_session(user_id):
    session_id = os.urandom(16).hex()  # Securely generates a random session ID
    session['user_id'] = user_id
    session['session_id'] = session_id
    return session_id

def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.headers.get('Session-ID')
        if not session_id or not session.get('session_id') == session_id:
            return jsonify({"error": "Unauthorized access"}), 401

        # If session is valid, proceed with the original function
        return func(*args, **kwargs)
    return wrapper

# You will need to add 'username' field to the User model for this to work
