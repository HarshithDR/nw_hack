# import requests

# url = "http://127.0.0.1:5000/upload-image"
# files = {'image': open('test.jpg', 'rb')}

# response = requests.post(url, files=files)
# print(response.json())


import json
import base64
import os
from datetime import datetime

def create_test_image_json(raspberry_pi_id="test_rpi", image_path="test.jpg", output_filename="test_upload.json"):
    """
    Creates a JSON file with the format expected by the Flask backend,
    including a Base64 encoded image.

    Args:
        raspberry_pi_id (str): The identifier for the Raspberry Pi.
        image_path (str): The path to the image file to encode.
        output_filename (str): The name of the JSON file to create.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        data = {
            'raspberryPi': raspberry_pi_id,
            'image': encoded_string,
        }

        with open(output_filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"JSON file '{output_filename}' created successfully.")

    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Create a dummy image file for testing (optional, but useful if you don't have one)
    # dummy_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\xfc\xff?\x03\x00\x01\xfa\xc9\xf7\x00\x00\x00\x00IEND\xaeB`\x82'
    # with open("test_image.png", "wb") as f:
    #     f.write(dummy_image_data)
    # print("Created a dummy test_image.png")

    # Create the test JSON file
    create_test_image_json()