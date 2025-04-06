from gen_ai import gemini_crop_recommendation, lat_long_finder
from db_functions import db_functions
import test_gemini
from io import BytesIO

def raspi_take_image():
    print('raspi_test')
    
def get_crop_recommendations(id, image, address):
    ### get address info from db
    address = None
    lat, long = lat_long_finder(address)
    recommneded_crops = gemini_crop_recommendation.main(image, lat, long)
    
def soil_test_and_crop_recommendation(id, file_id):
    print('soil analysis started')
    # address = db_functions.retrieve_address(id)
    # image = db_functions.get_image(file_id)

    # get_crop_recommendations(id, image, address)
    
    
soil_test_and_crop_recommendation("67f24f705a4e05f3bf038593", "temp_soil_img.jpg")
