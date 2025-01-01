import os
import json
from PIL import Image

import google.generativeai as genai

# working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# path of config_data file
config_file_path = f"{working_dir}/config.json"
config_data = json.load(open(config_file_path))

# loading the GOOGLE_API_KEY
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)


def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# get response from Gemini 1.5 Flash model - image/text to text
def gemini_pro_vision_response(prompt, image):
    gemini_flash_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_flash_model.generate_content([prompt, image])
    result = response.text
    return result

# get response from Gemini-Pro model - text to text
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result


# Example usage (commented out):
# result = gemini_pro_response("What is Machine Learning")
# print(result)
# print("-"*50)

# image = Image.open("test_image.png")
# result = gemini_pro_vision_response("Write a short caption for this image", image)
# print(result)
# print("-"*50)

# result = embeddings_model_response("Machine Learning is a subset of Artificial Intelligence")
# print(result)
