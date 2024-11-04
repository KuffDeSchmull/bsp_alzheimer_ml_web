from flask import Blueprint, request, jsonify, current_app
from models import User, Role, Test, PatientCaretakerRelation
from db import db
from datetime import datetime
from utils.authentication import start_session
import logging  # Import the logging module
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO)

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/create_patient', methods=['POST'])
def create_patient():
    data = request.json

    # Validate required fields
    if not all(k in data for k in ("name", "surname", "password", "gender", "birthDate")):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate gender
    if data['gender'] not in ['male', 'female', 'other']:
        return jsonify({"error": "Invalid gender"}), 400
    
     # Convert birthdate string to date object
    try:
        birthdate = datetime.strptime(data['birthDate'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid birthdate format"}), 400

    # Create new user
    new_user = User(
        name=data['name'],
        surname=data['surname'],
        gender=data['gender'],
        birthdate=birthdate
    )
    new_user.set_password(data['password'])

    # Add user to the database
    db.session.add(new_user)
    db.session.commit()

    # Create and add patient role
    patient_role = Role(id=new_user.id, role_type='patient')
    db.session.add(patient_role)
    db.session.commit()

    # Start a new session
    session_id = start_session(new_user.id)

    return jsonify({"message": "Patient created successfully", "user_id": new_user.id, "session_id": session_id}), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.json

    # Validate required fields
    if not all(k in data for k in ("name", "surname", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    # Fetch user from database
    user = User.query.filter_by(name=data['name'], surname=data['surname']).first()

    if user and user.check_password(data['password']):
        # Password is correct, start a new session
        session_id = start_session(user.id)
        return jsonify({"message": "Login successful", "session_id": session_id}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@user_blueprint.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        # Retrieve name and surname from request headers
        name = request.headers.get('Name')
        surname = request.headers.get('Surname')
        print(name)
        print(surname)

        if not name or not surname:
            return jsonify({"error": "Name and surname required"}), 400

        # Query the user by name and surname
        user = User.query.filter_by(name=name, surname=surname).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Get all tests associated with the user and delete the associated files
        tests = Test.query.filter_by(user_id=user.id).all()
        for test in tests:
            if test.file.endswith('.png'):
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], test.file)
            elif test.file.endswith('.json'):
                file_path = os.path.join(current_app.config['STROKES_FOLDER'], test.file)
            else:
                continue  # Skip if file extension is not recognized

            if os.path.exists(file_path):
                os.remove(file_path)
        # Delete associated tests
        Test.query.filter_by(user_id=user.id).delete()
        # Delete associated roles
        Role.query.filter_by(id=user.id).delete()
        # Delete patient-caretaker relations
        PatientCaretakerRelation.query.filter((PatientCaretakerRelation.patient_id == user.id) | (PatientCaretakerRelation.caretaker_id == user.id)).delete()

        # Delete the user
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error in delete_user: {e}")
        db.session.rollback()
        return jsonify({"error": "Unable to delete user"}), 500


