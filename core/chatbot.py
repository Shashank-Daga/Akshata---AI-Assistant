import json
import os
import google.generativeai as genai


# Loading API Key safely
def load_api_key():
    config_path = "config/settings.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError("Missing config/settings.json file with your Gemini API key.")

    with open(config_path, "r") as f:
        config = json.load(f)

    apiKey = config.get("gemini_api_key")
    if not apiKey:
        raise ValueError("Gemini API key not found in settings.json.")
    return apiKey


# Initialize Gemini Model
try:
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None


# Get assistant response
def get_chatbot_response(user_input):
    if not model:
        return "AI model is not available. Please check your API key and internet connection."

    try:
        response = model.generate_content(user_input)
        reply = response.text
        return reply.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm Sorry! I couldn't process the request at the moment."
