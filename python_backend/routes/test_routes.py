from flask import Blueprint, request, jsonify, current_app
from utils.authentication import check_session
from models import User
#from werkzeug.utils import secure_filename
import os
import secrets
import json
import base64
from PIL import Image
import io
from models import create_test,get_tests_by_session_and_extension,update_test,get_test, create_localization, del_localization, localization_get
from utils.evaluate import run_cnn_model

test_blueprint = Blueprint('test_blueprint', __name__)

def load_protocol(file_name, language):
    try:
        base = current_app.config['BASE_DIR']
        path = os.path.join(base, f'{language}protocols')
        
        with open(os.path.join(path, file_name), 'r') as file:
            return json.load(file)
    except IOError:
        return None

@test_blueprint.route('/protocol/<string:test_type>/<string:variant>', methods=['GET']) ##generic test protocol fetching, e.g. protocol/cdt/cnn
@check_session
def get_test_protocol(test_type, variant):
    language = request.headers.get('language', '')
    if language != '':
        language = language + '/'
    protocol = load_protocol(f"{test_type}_{variant}.json", language)
    if protocol:
        return jsonify(protocol)
    else:
        return jsonify({"error": "Protocol not found"}), 404
    
@test_blueprint.route('/get_protocols', methods=['GET'])
@check_session
def get_all_protocols():
    language = request.headers.get('language', '')
    if language != '':
        language = language + '/'
    base = current_app.config['BASE_DIR']
    protocols_folder = os.path.join(base, f'{language}protocols')
    ##protocols_folder = current_app.config['PROTOCOLS_FOLDER']
    protocols = {}
    for filename in os.listdir(protocols_folder):
        if filename.endswith('.json'):
            protocol_path = os.path.join(protocols_folder, filename)
            protocol = load_protocol(filename, language)
            if protocol:
                protocol_name = filename[:-5]  # Remove '.json' extension
                protocols[protocol_name] = protocol
    return jsonify(protocols)   

@test_blueprint.route('/upload', methods=['POST'])
@check_session
def upload_image():
    try:
        data = request.get_json()
        # Retrieve user identity from headers
        name = request.headers.get('Name')
        surname = request.headers.get('Surname')
        testname = request.headers.get('Test')
        timer = request.headers.get('Timer')

        try:
            result_time = float(timer)
        except (TypeError, ValueError):
            result_time = None
        # Find user by name and surname
        user = User.query.filter_by(name=name, surname=surname).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if 'imageData' not in data:
            return jsonify({'error': 'No image data found'}), 400
        # Extract the Base64 encoded data from the payload
        base64_string = data['imageData']
        # Check and remove the "data:image/png;base64," part
        if base64_string.startswith('data:image/png;base64,'):
            base64_string = base64_string.replace('data:image/png;base64,', '')
        # Decode the Base64 string
        image_data = base64.b64decode(base64_string)
        # Process the image
        image = Image.open(io.BytesIO(image_data))
        # Use session ID as filename
        session_id = request.headers.get('Session-ID')
        random_str = secrets.token_hex(8)
        filename = f'{session_id}_{random_str}.png'  # or generate a unique filename
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        # Create a new Test record
        newTestId = create_test(user.id, testname, None, result_time, None, filename)
        return jsonify({'message': 'Image uploaded successfully', 'testId': newTestId}) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@test_blueprint.route('/upload-strokes', methods=['POST'])
@check_session
def upload_strokes():
    try:
        data = request.get_json()
        if 'strokes' not in data:
            return jsonify({'error': 'No stroke data found'}), 400
        strokes = data['strokes']
        # Retrieve user identity from headers
        name = request.headers.get('Name')
        surname = request.headers.get('Surname')

        # Find user by name and surname
        user = User.query.filter_by(name=name, surname=surname).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        # Use session ID as filename
        session_id = request.headers.get('Session-ID')
        random_str = secrets.token_hex(8)
        filename = f'{session_id}_{random_str}.json'  # or generate a unique filename
        filepath = os.path.join(current_app.config['STROKES_FOLDER'], filename)
        # Save the strokes data to a JSON file
        create_test(user.id, 'cdt', None, None, None, filename)  
        with open(filepath, 'w') as file:
            json.dump(strokes, file, indent=4)  
        return jsonify({'message': 'Strokes data uploaded successfully', 'strokesPath': filepath})
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@test_blueprint.route('/evaluate', methods=['POST'])
@check_session
def evaluate_tests():
    language = request.headers.get('language', '')
    if language != '':
        language = language + '/'
    data = request.get_json()
    test_ids = data.get('testIds')
    if not test_ids:
        return jsonify({'error': 'No Tests found'}), 400

    session_id = request.headers.get('Session-ID')
    if not session_id:
        return jsonify({'error': 'Session ID not found'}), 400

    #tests = get_tests_by_session_and_extension(session_id)
    tests = [get_test(test_id) for test_id in test_ids]
    if not all(tests):
        return jsonify({'error': 'One or more tests not found'}), 404
    
    protocol_file = f"{tests[0].type}_cnn.json"  # Assuming all tests have the same type
    protocol = load_protocol(protocol_file, language)
    if not protocol or 'tasks' not in protocol or len(protocol['tasks']) != len(tests):
        return jsonify({'error': 'Protocol error or task count mismatch'}), 500
    results = []
    for index, test in enumerate(tests):
        task = protocol['tasks'][index]
        model_name = task['model']
        preprocessing = task['preprocessing']
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], test.file)
        healthState = 0
        # Run ML model for the specific task
        task_name = task['name']
        result_time = test.resultTime
        best_percentage = 0
        best_label = None
        best_state = None
        #result_label, result_percentage = run_cnn_model(image_path, model_name)
        # Run all models and select the best result
        for model_name in task['models']:
            result_label, result_percentage = run_cnn_model(image_path, model_name, preprocessing)
            if result_percentage > best_percentage:
                best_percentage = result_percentage
                best_label = result_label
                best_state = protocol['healthStates'][result_label]
        update_test(test.id, resultLabel=best_label, resultPercentage=best_percentage)
        classes = len(protocol['healthStates'])
        #state = protocol['healthStates'][result_label]
        results.append({'label': best_label, 'percentage': best_percentage, 'state': best_state, 'time': result_time, 'name': task_name})
        healthState += best_label
    response_data = {'results': results}
    if healthState >= (len(tests)/2)*(classes-1)/2:   #may need adjustment if we add a class for unrelated images
        response_data['healthNotice'] = protocol['healthNotice']
    return jsonify(response_data)    

@test_blueprint.route('/setlocalize', methods=['POST'])
def set_localization():
    data = request.get_json()
    language = data.get('language')
    if not language:
        return jsonify({'error': 'No language provided'}), 400
    default = data.get('default')
    if not default:
        return jsonify({'error': 'No default provided'}), 400
    translation = data.get('translation')
    if not translation:
        return jsonify({'error': 'No translation provided'}), 400
    # Create localization object
    localization = create_localization(default, translation, language)
    return jsonify({'message': 'Localization set successfully'})

@test_blueprint.route('/dellocalize', methods=['POST'])
def delete_localization():
    data = request.get_json()
    id = data.get('id')
    localization = del_localization(id)
    return jsonify({'message': 'Localization deleted successfully'})

@test_blueprint.route('/getlocalization', methods=['POST'])
def get_localization():
    language = request.headers.get('language', '')
    if language == '' or language == 'default' or language is None:
        language = 'en'
    if language == 'esp':
        language = 'es'
    data = request.get_json()
    default = data.get('default')
    localization = localization_get(language, default)
    if not localization:
        return jsonify({'error': 'Localization not found'}), 404
    translation = localization.translation
    return jsonify({'translation': translation})