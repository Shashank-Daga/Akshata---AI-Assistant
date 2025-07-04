import json
import google.generativeai as genai


# Loading API Key
def load_api_key():
    with open("config/settings.json", "r") as f:
        config = json.load(f)
    return config["gemini_api_key"]


# Initialize
api_key = load_api_key()
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def get_chatbot_response(user_input):
    try:
        response = model.generate_content(user_input)
        reply = response.text
        return reply.strip()

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm Sorry!, I couldn't process the request at the moment."
