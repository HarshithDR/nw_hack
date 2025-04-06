from gen_ai import gemini_crop_recommendation, lat_long_finder
from db_functions import db_functions
import test_gemini
from io import BytesIO
import json

def raspi_take_image():
    print('raspi_test')
    
def get_crop_recommendations(id, image, address):
    ### get address info from db
    address = None
    lat, long = lat_long_finder.get_coordinates(address)
    recommneded_crops = gemini_crop_recommendation.main(image, lat, long)
    print(f"Recommended crops to grow: {json.dumps(recommneded_crops)}")
    return {"Recommended crops": json.dumps(recommneded_crops)}
    
    
def soil_test_and_crop_recommendation(id, file_id):
    print('soil analysis started')

    address = db_functions.retrieve_address('67f24f705a4e05f3bf038593')
    image = db_functions.get_image(file_id)

    recommended_crops = get_crop_recommendations(id, image, address)
    return recommended_crops
    
# # soil_test_and_crop_recommendation("67f24f705a4e05f3bf038593", "temp_soil_img.jpg")
# image = db_functions.get_image("temp_soil_img.jpg")
# x = test_gemini.process_image(image, "what is this image?")
# print(x)