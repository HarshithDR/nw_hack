import sys 
sys.path.append('../')

import google.generativeai as genai
import json
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()


def process_image(image_path:str, prompt:str):
    
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    img = Image.open(image_path)
    
    response = model.generate_content([prompt, img])
    
    result = {
        "result": response.text
        }
    
    return json.dumps(result)

def roadmap_from_image(analysis_json:str, roadmap_prompt=str):
    analyze_data = json.loads(analysis_json)
    description = analyze_data.get('result')
    
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    formatted_prompt = roadmap_prompt.format(description=description)
    response = model.generate_content(formatted_prompt)
    
    result = {
        "roadmap": response.text,
        "original_description": description
    }

    return json.dumps(result, indent=2)


if __name__ =="__main__":
    image_path = "shirt.jpg"
    
    prompt = "What is in the image, describe in simple english"
    
    result = process_image(image_path, prompt)
    
    ROADMAP_PROMPT = """Create a detailed 12-month implementation roadmap for this project:
    {description}
    Include phases, milestones, and key deliverables. Format the roadmap in clear chronological stages."""
    
    roadmap = roadmap_from_image(result, ROADMAP_PROMPT)
    
    print(roadmap)