import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

def process_image(image: bytes, prompt: str):
    """Process the image using Gemini 1.5 Flash and get recommendations"""
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Load image using Pillow
    # image = Image.open(io.BytesIO(image_bytes))

    # Pass Pillow image directly
    response = model.generate_content([
        image,  # Passing Pillow Image object
        prompt
    ])
    
    return json.dumps({"result": response.text})
