from flask_bcrypt import Bcrypt
from db import db
from datetime import datetime
import logging
# Setup basic logging
logging.basicConfig(level=logging.INFO)


bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birthdate = db.Column(db.Date)
    condition = db.Column(db.String(50))
    isDiagnosed = db.Column(db.String(50))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Role(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_type = db.Column(db.Enum('admin', 'patient', 'caretaker', name='role_types'))
class PatientCaretakerRelation(db.Model):
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    caretaker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    type = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    resultLabel = db.Column(db.String(50))
    resultTime = db.Column(db.Float)
    resultPercentage = db.Column(db.Float)
    file = db.Column(db.String(200))
    # Relationship (optional, for back-referencing)
    user = db.relationship('User', backref=db.backref('tests', lazy=True))

class Localization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.String(500))
    translation = db.Column(db.String(500))
    language = db.Column(db.String(10))

def create_localization(default, translation, language):
    new_localization = Localization(default=default, translation=translation, language=language)
    db.session.add(new_localization)
    db.session.commit()


def localization_get(language, default):
    localization = Localization.query.filter_by(language=language, default=default).first()
    if localization:
        return localization
    else:
        return None
    
def del_localization(id):
    localization = Localization.query.get(id)
    if localization:
        db.session.delete(localization)
        db.session.commit()
        return True
    else:
        return False

def create_user(name, surname, password, gender, birthdate):
    new_user = User(name=name, surname=surname, gender=gender, birthdate=birthdate)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if user:
        # Update user attributes based on kwargs
        # For example, if 'name' in kwargs: user.name = kwargs['name']
        db.session.commit()
    # Handle user not found or return updated user


def assign_caretaker(patient_id, caretaker_id):
    patient = User.query.get(patient_id)
    caretaker = User.query.get(caretaker_id)
    if patient and caretaker:
        # Further checks can be added here
        relation = PatientCaretakerRelation(patient_id=patient_id, caretaker_id=caretaker_id)
        db.session.add(relation)
        db.session.commit()
    else:
        # Handle the case where either patient or caretaker does not exist
        pass


def create_test(user_id, type, resultLabel, resultTime, resultPercentage, file):

    try:
        logging.info(f"Creating test: user_id={user_id}, type={type}, file={file}")

        new_test = Test(
            user_id=user_id,
            type=type,
            timestamp=datetime.now(),
            resultLabel=resultLabel,
            resultTime=resultTime,
            resultPercentage=resultPercentage,
            file=file
        )

        db.session.add(new_test)
        db.session.commit()

        logging.info(f"Test created successfully with ID: {new_test.id}")
        return new_test.id

    except Exception as e:
        logging.error(f"Error in create_test: {e}")
        db.session.rollback()  # Rollback the transaction in case of error
        return None

def get_test(test_id):
    test = Test.query.get(test_id)
    if test:
        return test
    else:
        return None  # or handle as needed

def update_test(test_id, resultLabel=None, resultPercentage=None):
    try:
        test = Test.query.get(test_id)
        if test:
            if resultLabel is not None:
                test.resultLabel = resultLabel
            if resultPercentage is not None:
                test.resultPercentage = resultPercentage
            db.session.commit()
            logging.info(f"Test updated successfully: {test_id}")
        else:
            logging.error(f"Test not found: {test_id}")
    except Exception as e:
        logging.error(f"Error in update_test: {e}")
        db.session.rollback()


def get_tests_by_session_and_extension(session_id, extension='.png'):
    try:
        tests = Test.query.filter(Test.file.like(f'{session_id}%{extension}')).all()
        return tests
    except Exception as e:
        logging.error(f"Error in get_tests_by_session_and_extension: {e}")
        return []


