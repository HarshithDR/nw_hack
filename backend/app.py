from flask import Flask, request, jsonify
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
import call_functions
from io import BytesIO
from flask import send_file
# import db_functions
from db_init import db_functions

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
        db_functions.add_profile(id.get('_id'), land_location, land_area)
        return jsonify({'id': id.get('_id')}), 200
    else:
        return jsonify({"error": "creating user"}), 500


@app.route('/soil_details', methods=['POST'])
def soil_details():
    """json accepts:
    raspberrypi: Yes or No
    image: base64 encoded image string"""
    
    try:
        data = request.get_json()
        raspberry_pi = data.get('raspberrypi')
        
        if raspberry_pi == 'Yes':
            call_functions.raspi_take_image()
            call_functions.soil_test()
            return jsonify({'message': "Requested for Raspberry Pi to take photo and analyze"}), 200
            
        else:
            base64_image = data.get('image')
        
            if not base64_image:
                return jsonify({'error': 'Image data is missing'}), 400

            try:
                # Decode the base64 string
                image_bytes = base64.b64decode(base64_image)
            except Exception as e:
                return jsonify({'error': f'Invalid Base64 image data: {str(e)}'}), 400
            
            filename = "temp_soil_img.jpg"  # You can customize the filename if needed
            
            # Upload the image to GridFS
            file_id = db_functions.upload_image(image_bytes, filename)
            
            if file_id:
                call_functions.soil_test()
                return jsonify({'message': 'Image received and saved to GridFS successfully', 'filename': filename, 'file_id': str(file_id)}), 200
            else:
                return jsonify({'error': 'Failed to upload image to GridFS'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    
@app.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    file_data = db_functions.get_image(filename)
    if file_data:
        return send_file(BytesIO(file_data), download_name=filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)