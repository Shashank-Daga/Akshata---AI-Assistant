import os
from datetime import datetime

# Define paths
ACTION_LOG_PATH = "logs/actions.log"
CONVERSATION_LOG_PATH = "logs/conversation_history.txt"

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)


# Log generic assistant actions (used like before)
def log_action(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ACTION_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


# Log conversation (user input and assistant response)
def log_interaction(user_input, assistant_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CONVERSATION_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {assistant_response}\n")
        f.write("-" * 40 + "\n")


# Retrieve full assistant memory / conversation history
def read_log():
    if not os.path.exists(CONVERSATION_LOG_PATH):
        return "No conversation history found."
    with open(CONVERSATION_LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()


# 🧠 Filtered memory viewer
def get_filtered_memory_logs(date_filter=None, keyword_filter=None, type_filter=None):
    results = []
    log_file = CONVERSATION_LOG_PATH  # Fixed path

    if not os.path.exists(log_file):
        return results

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entry = []
    for line in lines:
        if line.strip() == "-" * 40:
            block = "".join(entry)
            if date_filter and date_filter not in block:
                entry = []
                continue
            if keyword_filter and keyword_filter.lower() not in block.lower():
                entry = []
                continue
            if type_filter and type_filter.lower() not in block.lower():
                entry = []
                continue
            results.append(block.strip())
            entry = []
        else:
            entry.append(line)

    return results
