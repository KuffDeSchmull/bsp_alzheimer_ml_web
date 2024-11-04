from flask import Flask
import os
from flask_cors import CORS

from db import db

from routes.user_routes import user_blueprint
from routes.test_routes import test_blueprint

app = Flask(__name__)
app.secret_key = 'your_very_secret_key' #change this later, use env variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mldiagnostics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


# Get the directory where the server.py file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the upload folder path relative to the base directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'images')
STROKES_FOLDER = os.path.join(BASE_DIR, 'strokes')
PROTOCOLS_FOLDER = os.path.join(BASE_DIR, 'protocols')

db.init_app(app)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(test_blueprint, url_prefix='/test')

with app.app_context():
    db.create_all()

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(STROKES_FOLDER):
    os.makedirs(STROKES_FOLDER)

if not os.path.exists(PROTOCOLS_FOLDER):
    os.makedirs(PROTOCOLS_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STROKES_FOLDER'] = STROKES_FOLDER       
app.config['PROTOCOLS_FOLDER'] = PROTOCOLS_FOLDER  
app.config['BASE_DIR'] = BASE_DIR

if __name__ == '__main__':
    app.run(debug=True)
