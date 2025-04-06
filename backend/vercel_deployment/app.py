from flask import Flask, request, jsonify
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
from call_functions import call_functions
from io import BytesIO
from flask_cors import CORS  
from flask import send_file
from db_functions import db_functions

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = db_functions.validate_login(username, password)
    if user:
        return jsonify({'id': str(user.get('_id'))}), 200
    else:
        return jsonify({"error": "Login credentials don't match"}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    land_area = data.get('land_area')
    land_location = data.get('land_location')
    
    user = db_functions.create_user(username, password)
    if user:
        db_functions.create_profile(str(user.get('_id')), land_location, land_area)
        return jsonify({'id': str(user.get('_id'))}), 200
    else:
        return jsonify({"error": "Error creating user"}), 500

@app.route('/soil_details', methods=['POST'])
def soil_details():
    try:
        data = request.get_json()
        raspberry_pi = data.get('raspberrypi')
        
        if raspberry_pi == 'Yes':
            call_functions.raspi_take_image()
            results = call_functions.soil_test()
            return jsonify(results), 200
        else:
            base64_image = data.get('image')
            if not base64_image:
                return jsonify({'error': 'Image data is missing'}), 400

            image_bytes = base64.b64decode(base64_image)
            filename = f"soil_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            
            file_id = db_functions.upload_image(image_bytes, filename)
            if file_id:
                results = call_functions.soil_test()
                return jsonify({
                    'message': 'Image received and analyzed',
                    'results': results,
                    'file_id': str(file_id)
                }), 200
            return jsonify({'error': 'Failed to process image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def vercel_handler(request):
    from flask import Response
    with app.app_context():
        response = app.full_dispatch_request()
        return Response(
            response=response.get_data(),
            status=response.status_code,
            headers=dict(response.headers)
        )

if __name__ == '__main__':
    app.run(debug=True)