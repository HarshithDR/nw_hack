import time
import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from dotenv import load_dotenv
import os
import json
from PIL import Image
from io import BytesIO
import base64
import re
from datetime import datetime
import os
import json
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
IP_WEBCAM_URL = os.environ.get('IP_WEBCAM_URL')
BACKEND_URL = os.environ.get('BACKEND_URL')

def process_image(image: bytes, prompt: str):
    """Process the image using Gemini 1.5 Flash and get recommendations"""
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    model = genai.GenerativeModel('gemini-1.5-flash')

    # img = Image.open(image_path)

    response = model.generate_content([image, prompt])

    result_text = response.text
    # Extract the JSON string from the markdown
    json_match = re.search(r'```json\n(.*)\n```', result_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {json_match.group(1)}")
            return {"error": "Failed to decode JSON"}
    else:
        print(f"Could not find JSON in the response: {result_text}")
        return {"error": "JSON not found in response"}


import numpy as np  # Import numpy for easier mean calculation

def recommend_crops(weather_data, image):
    """Use the data to dynamically recommend crops based on weather data"""
    if not weather_data:
        weather_summary = "No weather data available."
    else:
        temperatures = [item.get('temperature_2m') for item in weather_data if isinstance(item, dict) and 'temperature_2m' in item and item['temperature_2m'] is not None]
        rains = [item.get('rain') for item in weather_data if isinstance(item, dict) and 'rain' in item and item['rain'] is not None]
        humidities = [item.get('relative_humidity_2m') for item in weather_data if isinstance(item, dict) and 'relative_humidity_2m' in item and item['relative_humidity_2m'] is not None]
        precipitations = [item.get('precipitation') for item in weather_data if isinstance(item, dict) and 'precipitation' in item and item['precipitation'] is not None]

        avg_temp = np.mean(temperatures) if temperatures else 'N/A'
        avg_rain = np.mean(rains) if rains else 'N/A'
        avg_humidity = np.mean(humidities) if humidities else 'N/A'
        avg_precipitation = np.mean(precipitations) if precipitations else 'N/A'

        weather_summary = f"The average temperature is {avg_temp}°C, " \
                            f"average rainfall is {avg_rain} mm, " \
                            f"relative humidity is {avg_humidity}%, " \
                            f"and precipitation is {avg_precipitation} mm."

    prompt = f"Given the weather conditions ({weather_summary}), just give the name of the crops as a JSON array that would be suitable to grow in this environment?. I do not want any explanation of the same"
    return process_image(image, prompt)


def gemi_main_crop_pred(image, weather_data):
    recommended_crops_raw = recommend_crops(weather_data, image)

    if isinstance(recommended_crops_raw, dict) and "error" in recommended_crops_raw:
        return recommended_crops_raw
    elif isinstance(recommended_crops_raw, list):
        return {"recommended_crops": recommended_crops_raw}
    else:
        return {"error": "Unexpected format of recommended crops"}


def take_photo():
    try:
        response = requests.get(IP_WEBCAM_URL)
        print("running take photo")
        image = Image.open(BytesIO(response.content))
         
        # Save the image
        filename = "captured_image.jpg"
        image.save(filename)
        
        weather_data = requests.get(BACKEND_URL + "/fetch_weather")
        if weather_data.status_code == 200:
            weather_data = weather_data.json().get('data')
            
        recommended_crops_output = gemi_main_crop_pred(filename,weather_data)
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(BACKEND_URL + '/get_crop_pred', headers=headers, json=json.dumps(recommended_crops_output))
        # print(f"Photo saved as {filename}")
        # with open(filename, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # data = {
        #     'number':1,
        #     'image': encoded_string
        # }
        
        # try:
        #     #print(json.dumps(data))
        #     headers = {'Content-Type': 'application/json'}
        #     response = requests.post(BACKEND_URL + '/upload_image_from_raspi_for_soil_testing', headers=headers, json=json.dumps(data))

        #     #response = requests.post(BACKEND_URL + '/upload_image_from_raspi_for_soil_testing', json=json.dumps(data))
        #     print(response.status_code)
        # except Exception as e:
        #     print(e)
        # # Show the image (optional)
        # # image.show()
        # return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def check_backend_to_take_photo():
    while True:
        try:
            response = requests.get(BACKEND_URL + "/check_if_photo_needed")
            if response.status_code == 200 and response.json().get("take_photo"):
                photo_taken = take_photo()
                if photo_taken:
                    print("photo taken as per backend manual request")
        except requests.RequestException as e:
            print(f"Error connecting to backend: {e}")
        time.sleep(5)  # Ping backend every 5 seconds

def scheduled_task():
    photo_taken = take_photo()

if __name__ == "__main__":
    print("starting raspberry pi server")
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=1)
    scheduler.start()

    backend_thread = threading.Thread(target=check_backend_to_take_photo)
    backend_thread.daemon = True
    backend_thread.daemon = True
    backend_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        scheduler.shutdown()
