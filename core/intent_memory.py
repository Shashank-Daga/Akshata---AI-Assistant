import json
import os

INTENT_FILE = "data/intent_memory.json"


# Load or create file
def load_intent():
    if os.path.exists(INTENT_FILE):
        with open(INTENT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_intents(intents):
    with open(INTENT_FILE, "w") as f:
        json.dump(intents, f, indent=2)


# Add new intent
def add_intent(user_phrase, cmd):
    intents = load_intent()
    intents[user_phrase.lower()] = cmd
    save_intents(intents)


# Try to match user input
def match_intent(user_input):
    intents = load_intent()
    for phrase, cmd in intents.items():
        if phrase in user_input.lower():
            return cmd
    return None
