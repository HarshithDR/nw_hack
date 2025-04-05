from flask import Flask, request, jsonify
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
import call_functions

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_images'  # Directory to save uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/soil_details', methods=['POST'])
def soil_details():
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


# @app.route('/get-data', methods=['GET'])
# def get_data():
#     return jsonify({"message": "This is a GET request"})

# @app.route('/post-data', methods=['POST'])
# def post_data():
#     data = request.get_json()
#     return jsonify({"received": data}), 201

if __name__ == '__main__':
    app.run(debug=True)