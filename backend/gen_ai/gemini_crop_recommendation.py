import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
import os
import json
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather_data(latitude, longitude):
    """Fetch weather data for a given latitude and longitude"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Weather API params
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2024-04-21",
        "end_date": current_date,
        "hourly": ["temperature_2m", "rain", "relative_humidity_2m", "precipitation"],
        "utm_source": "chatgpt.com"
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process the first location
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    hourly_dataframe['month'] = hourly_dataframe['date'].dt.month_name()

    # Group by month and calculate the average
    monthly_averages = hourly_dataframe.groupby('month').agg({
        'temperature_2m': 'mean',
        'rain': 'mean',
        'relative_humidity_2m': 'mean',
        'precipitation': 'mean'
    }).reset_index()

    # Sort the months in calendar order
    monthly_averages['month'] = pd.Categorical(monthly_averages['month'], categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    monthly_averages = monthly_averages.sort_values('month').reset_index(drop=True)
    
    return monthly_averages


def process_image(image_path:str, prompt:str):
    """Process the image using Gemini 1.5 Flash and get recommendations"""
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    img = Image.open(image_path)
    
    response = model.generate_content([prompt, img])
    
    result = {
        "result": response.text
    }
    
    return json.dumps(result)


def recommend_crops(weather_data, image_path):
    """Use the data to dynamically recommend crops based on weather data"""
    # Prepare the input prompt for Gemini 1.5 based on the weather data
    weather_summary = f"The average temperature is {weather_data['temperature_2m'].mean()}°C, " \
                      f"average rainfall is {weather_data['rain'].mean()} mm, " \
                      f"relative humidity is {weather_data['relative_humidity_2m'].mean()}%, " \
                      f"and precipitation is {weather_data['precipitation'].mean()} mm."

    prompt = f"Given the weather conditions ({weather_summary}), just gave the name of the crops as a JSON string that would be suitable to grow in this environment?. I do not want any explanation of the same"

    return process_image(image_path, prompt)


def main(image_path, latitude, longitude):
    weather_data = get_weather_data(latitude, longitude)
    recommended_crops = recommend_crops(weather_data, image_path)
    
    return recommended_crops


image_path = 'red_soil.jpg' 
latitude = 52.52
longitude = 13.41

recommended_crops = main(image_path, latitude, longitude)
print(f"Recommended crops to grow: {recommended_crops}")
