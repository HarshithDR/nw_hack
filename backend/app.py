from flask import Flask, request, jsonify
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
import call_functions
import db_functions

load_dotenv()

app = Flask(__name__)
    
@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    id = db_functions.validate_login(username, password)
    if id:
        return jsonify({'id': id.get('_id')}), 200
    else:
        return jsonify({"error": "Login credentials don't match"}), 500

    
@app.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    land_area = data.get('land_area')
    land_location = data.get('land_location')
    
    id = db_functions.create_user(username, password)
    if id:
        db_functions.add_profile(id.get('_id'), land_area, land_location)
        return jsonify({'id': id.get('_id')}), 200
    else:
        return jsonify({"error": "creating user"}), 500


@app.route('/soil_details', methods=['POST'])
def soil_details():
    """json accepts: 
    raspberrypi : Yes or No
    image: ....."""
    
    try:
        data = request.get_json()
        raspberry_pi = data.get('raspberrypi')
        
        if raspberry_pi == 'Yes':
            call_functions.raspi_take_image()
            call_functions.soil_test()
            return jsonify({'message': "requested for raspberry pi for take photo and analyse"}), 200
            
        else:
            base64_image = data.get('image')
        
            if not base64_image:
                return jsonify({'error': 'Image data is missing'}), 400

            try:
                image_bytes = base64.b64decode(base64_image)
            except Exception as e:
                return jsonify({'error': f'Invalid Base64 image data: {str(e)}'}), 400
            
            filename = f"temp_soil_img.jpg"  
            filepath = "temp_images/" + filename

            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            call_functions.soil_test()
            
        return jsonify({'message': 'Image received and saved successfully', 'filename': filename, 'raspberryPi': raspberry_pi}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    


if __name__ == '__main__':
    app.run(debug=True)