from flask import Flask, request, jsonify
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
import call_functions
from io import BytesIO
from flask import send_file
from gen_ai import weather_data_fetch
import time
# import db_functions
import json
from gen_ai import lat_long_finder, crop_yield_pre_reqs
from db_functions import db_functions

load_dotenv()
trigger_photo = False
d_id = None
rec_crop_list = {}

app = Flask(__name__)
    
@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    id = db_functions.validate_login(username, password)
    if id:
        global d_id
        d_id = id.get('_id')
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
        db_functions.create_profile(id.get('_id'), land_location, land_area)
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
        id = data.get('id')
        id  = '67f24f705a4e05f3bf038593'
        
        if raspberry_pi == 'Yes':
            global trigger_photo
            trigger_photo = True
            time.sleep(1)
            file_id = "temp_soil_img.jpg"
            call_functions.soil_test_and_crop_recommendation(id, file_id)
            recommended_crops = call_functions.soil_test_and_crop_recommendation(id, file_id)
            return recommended_crops, 200
            
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
                recommended_crops = call_functions.soil_test_and_crop_recommendation(id, file_id)
                return recommended_crops, 200
            else:
                return jsonify({'error': 'Failed to upload image to GridFS'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    
@app.route('/select_crop', methods = ['POST'])
def select_crop():
    data = request.get_json()
    id = data.get('id')
    crop = data.get('selected_crop')
    try:
        db_functions.update_crop_selection_to_user_profile(id, crop)
        return jsonify({"message":"updated profile section with crop"}), 200
    except Exception as e:
        return jsonify({"error":e}), 500
    
    
@app.route('/crop_yield', methods = ['POST'])
def crop_yield():
    data = request.get_json()
    id = data.get('id')
    acres = db_functions.retrieve_acres(id)
    crop = db_functions.retrieve_crop(id)
    preds = json.loads(crop_yield_pre_reqs.prompt_gemini_for_crop(crop, acres))
    return jsonify({"preds": preds}), 200


@app.route('/roadmap', methods = ['POST'])
def roadmap():
    data = request.get_json()
    id = data.get('id')
    
    crop = db_functions.retrieve_crop(id)
    roadmap_data = crop_yield_pre_reqs(crop)
    
    return jsonify({"data": roadmap_data}), data
    
    
    
@app.route('/check_if_photo_needed', methods = ['GET'])
def check_if_photo_needed():
    print('rapberry pi requested')
    if trigger_photo:
        return jsonify({'take_photo':True}), 200
    return jsonify({"error": "trigger not detected"}), 500

@app.route('/upload_image_from_raspi_for_soil_testing', methods = ['POST'])
def upload_image_from_raspi_for_soil_testing():
    data = request.get_json()
    data = json.loads(data)
    # print(type(data))
    # image = data.get('image')
    b_image = data.get('image')
        
    if not b_image:
        return jsonify({'error': 'Image data is missing'}), 400
    try:
        # Decode the base64 string
        image_bytes = base64.b64decode(b_image)
    except Exception as e:
        return jsonify({'error': f'Invalid Base64 image data: {str(e)}'}), 400

    filename = "temp_soil_img.jpg"  # You can customize the filename if needed
    
    # Upload the image to GridFS
    file_id = db_functions.upload_image(image_bytes, filename)
    
    if file_id:
        call_functions.soil_test_and_crop_recommendation(id, file_id)
        return jsonify({'message': 'Image received and saved to GridFS successfully', 'filename': filename, 'file_id': str(file_id)}), 200
    else:
        return jsonify({'error': 'Failed to upload image to GridFS'}), 500
# @app.route('/get_image/<filename>', methods=['GET'])
# def get_image(filename):
#     file_data = db_functions.get_image(filename)
#     if file_data:
#         return send_file(BytesIO(file_data), download_name=filename, as_attachment=True)
#     else:
#         return jsonify({"error": "File not found"}), 404

# @app.route('/fetch_weather', methods = ['GET'])
# def featch_weather():
#     address = db_functions.retrieve_address(d_id)
#     lat, long = lat_long_finder.get_coordinates(address)
#     weather_data = weather_data_fetch.get_weather_data(lat, long)
#     weather_data_json = weather_data.to_dict(orient='records')
#     return jsonify({"data": weather_data_json}), 200


# @app.route('/get_crop_pred', methods = ['POST'])
# def get_crop_pred():
#     data = request.get_data()
#     global rec_crop_list
#     rec_crop_list = data
    
#     return jsonify({"message": "got your recommendations"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000, debug=True) 