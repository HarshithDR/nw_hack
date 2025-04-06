import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Make sure all required weather variables are listed here
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "start_date": "2024-04-21",
    "end_date": current_date,
    "hourly": ["temperature_2m", "rain", "relative_humidity_2m", "precipitation"],
    "utm_source": "chatgpt.com"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
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

# Convert the 'date' column to datetime if it's not already
hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])

# Extract the month from the 'date' column
hourly_dataframe['month'] = hourly_dataframe['date'].dt.month_name()

# Group by month and calculate the average for each parameter
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

# Print monthly averages
print(monthly_averages)
