import json
import os

INTENT_FILE = "data/intent_memory.json"


# Load or create intent file
def load_intent():
    if os.path.exists(INTENT_FILE):
        try:
            with open(INTENT_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading intents: {e}")
            return {}
    return {}


def save_intents(intents):
    os.makedirs(os.path.dirname(INTENT_FILE), exist_ok=True)
    with open(INTENT_FILE, "w") as f:
        json.dump(intents, f, indent=2)


# Add a new learned intent
def add_intent(user_phrase, cmd):
    intents = load_intent()
    intents[user_phrase.lower()] = cmd
    save_intents(intents)


# Match the intent (exact or full sentence match)
def match_intent(user_input):
    intents = load_intent()
    user_input_lower = user_input.lower()
    for phrase, cmd in intents.items():
        if user_input_lower.strip() == phrase.strip():  # Exact match
            return cmd
        elif phrase in user_input_lower and len(phrase.split()) >= 2:  # Phrase match (min 2 words)
            return cmd
    return None
