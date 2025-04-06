import json
from typing import Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

dummy_profile_data = {
    "id": "67f209150029416ba26b1443",
    "geo_location": "123 s ave",
    "acres": "20"
}

dummy_user_history = [
    {
        "desc": "Rohan's first desc",
        "response": "Rohan's first response",
    },
    {
        "desc": "What crop should I grow in summer?",
        "response": "You can try growing corn or tomatoes."
    }
]

# def fetch_acres_and_history(user_id: str) -> Optional[tuple]:
#     """
#     Fetch acres and history from dummy JSON data.
#     """
#     try:
#         if dummy_profile_data["id"] != user_id:
#             print(f"No profile found for user ID: {user_id}")
#             return None

#         acres = float(dummy_profile_data.get("acres", 0))
#         history = [{"desc": doc.get("desc", ""), "response": doc.get("response", "")} for doc in dummy_user_history]

#         return acres, history

#     except Exception as e:
#         print(f"Error fetching user data: {e}")
#         return None

def prompt_gemini_for_crop(crop_name: str, acres: float) -> str:
    """
    Prompt Gemini 1.5 Flash to get a JSON response with crop details.
    """
    # history_text = "\n".join([f"Q: {h['desc']}\nA: {h['response']}" for h in history]) if history else "No prior interaction history."

    prompt = f"""
You're an expert agricultural consultant.

Given:
- Crop selected: {crop_name}
- Land size: {acres} acres
- Previous user conversations: 


Provide the following information as a JSON object with keys "Time to Harvest", "Cost", and "Yield". Each value should be a string with units (e.g., "5 months", "$2000", "10 tonnes"). Do not include any explanations, additional text, or markdown formatting. Only output the plain JSON object without any formatting.

Example:
{{
  "Time to Harvest": "5 months",
  "Cost": "$2000",
  "Yield": "10 tonnes"
}}
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return json.dumps({"error": f"Error generating Gemini response: {e}"})

def get_crop_recommendation_for_user(crop_name: str, user_id: str) -> str:
    """
    Main function to fetch data and return Gemini's crop recommendation as JSON.
    """
    result = fetch_acres_and_history(user_id)
    if not result:
        return json.dumps({"error": "Could not fetch user data."})

    acres, history = result
    return prompt_gemini_for_crop(crop_name, acres, history)

def get_crop_roadmap(crop_name: str) -> dict:
    """
    Prompt Gemini to get a roadmap from seeding to harvest based on cost, time, and yield.
    The output is a JSON with textual keys and values, in chronological order.
    """
    # pre_info_json = json.dumps(pre_info)
    prompt = f"""
You're an expert agricultural advisor.

Given the following details for the crop "{crop_name}":

Provide a step-by-step roadmap to grow this crop from seeding to harvest. Return the answer in a JSON format where:
- The keys are short sentences describing each step in chronological order.
- The values explain what should be done in that step (concise and clear).
- The entire content should be only plain text. No formatting, no special characters, no bullet points.

Only return a valid JSON. Do not include any extra text before or after the JSON.
"""

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Failed to get response: {e}"}



if __name__ == "__main__":
    user_id = "67f209150029416ba26b1443"
    crop = "Wheat"
    output = get_crop_recommendation_for_user(crop, user_id)
    print(output)
    
    roadmap = get_crop_roadmap(crop, output)
    print("🌾 Roadmap from Seeding to Harvest:\n")
    print(json.dumps(roadmap, indent=2))

    