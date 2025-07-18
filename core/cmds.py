import os
import subprocess
import webbrowser
import pyautogui
import re

from datetime import datetime
from core.permissions import requires_permission, request_permission_gui
from core.camera import take_photo, start_webcam
from core.intent_memory import match_intent, add_intent
from core.system_controls import set_volume_level, change_volume, mute_volume
from core.system_controls import set_brightness, change_brightness
from core.window_manager import (
    minimize_all_windows,
    maximize_current_window,
    minimize_current_window,
    close_current_window,
    close_all_windows,
    snap_active_window,
    close_specific_app,
    switch_window,
    open_task_manager
)
from core.recent_files import get_recent_files
from core.reminder import handle_reminder_cmd
from core.internet_tools.calculator import evaluate_expression
from core.internet_tools.wikipedia import fetch_wikipedia_summary
from core.internet_tools.weather import get_weather_info
from core.tools import search_web, translate_text, launch_app

SEARCH_FOLDER = os.path.expanduser("~/Documents")  # Instead of hardcoded D:\\College


# 🔍 File Search
def search_file(key):
    for root, dirs, files in os.walk(SEARCH_FOLDER):
        for file in files:
            if key.lower() in file.lower():
                full_path = os.path.join(root, file)
                os.startfile(full_path)
                return f"Opened file: {file}"
    return f"No file found with keyword: {key}"


# 🚀 Main Command Execution
def exe_cmd(query):
    query = query.lower()

    # 🔒 Permission check
    if requires_permission(query):
        if not request_permission_gui():
            return "Permission denied."

    # 💡 Intent memory fallback
    learned_cmd = match_intent(query)
    if learned_cmd:
        return exe_cmd(learned_cmd)

    # 🧠 Intent learning command
    if query.startswith("remember when i say"):
        try:
            parts = query.split("i mean")
            user_phrase = parts[0].replace("remember when i say", "").strip()
            mapped_cmd = parts[1].strip()
            add_intent(user_phrase, mapped_cmd)
            return f"Got it! I'll remember '{user_phrase}' means '{mapped_cmd}'."
        except:
            return "Sorry, I couldn't understand the intent mapping."

    # Reminder Handling
    reminder_response = handle_reminder_cmd(query)
    if reminder_response:
        return reminder_response

    # 📂 Application Commands
    elif "open notepad" in query:
        os.system("notepad")
        return "Opening Notepad."

    elif "open chrome" in query or "open browser" in query:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path])
            return "Opening Google Chrome."
        return "Chrome path not found."

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "search google for" in query:
        search_term = query.split("search google for")[-1].strip()
        if search_term:
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            return f"Searching Google for '{search_term}'."
        return "Please specify a search query."

    elif "play on youtube" in query:
        song = query.split("play on youtube")[-1].strip()
        if song:
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            return f"Playing {song} on YouTube."
        return "Please specify what to play."

    elif query.startswith("open ") or query.startswith("launch "):
        app_name = query.split(" ", 1)[-1]
        return launch_app(app_name)

    # Web Search
    if query.startswith("search for"):
        query = query.replace("search for", "").strip()
        return search_web(query)

    # Translation
    if query.startswith("translate "):
        parts = query.split(" to ")
        if len(parts) == 2:
            text = parts[0].replace("translate", "").strip()
            target = parts[1].strip()
            return translate_text(text, target)
        else:
            return "Please specify text and target language like: 'translate hello to spanish'"

    # 📁 File Search
    elif "search file" in query or "open file" in query:
        key = query.split("file")[-1].strip()
        if not key:
            return "Please specify the file name."
        return search_file(key)

    # 🪟 Window Manager
    elif "minimize all" in query:
        return minimize_all_windows()

    elif "maximize window" in query or "maximize current window" in query:
        return maximize_current_window()

    elif "minimize window" in query or "minimize current window" in query:
        return minimize_current_window()

    elif "close window" in query or "close current window" in query:
        return close_current_window()

    elif "close all windows" in query:
        return close_all_windows()

    elif "snap window to left" in query:
        return snap_active_window("left")

    elif "snap window to right" in query:
        return snap_active_window("right")

    elif "close all" in query and "windows" in query:
        app = query.replace("close all", "").replace("windows", "").strip()
        if app.lower() == "windows":
            return close_all_windows()
        else:
            return close_specific_app(app)

    elif "switch window" in query:
        return switch_window()

    elif "open task manager" in query:
        return open_task_manager()

    # 🖼️ Camera / Screenshot
    elif "take screenshot" in query:
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(folder, f"screenshot_{timestamp}.png")
        pyautogui.screenshot(filepath)
        return f"Screenshot saved as {filepath}"

    elif "take photo" in query or "take a picture" in query:
        return take_photo()

    elif "start webcam" in query or "open camera" in query:
        return start_webcam()

    # 🔊 Volume
    elif "increase volume" in query:
        change_volume(up=True)
        return "Volume increased."

    elif "decrease volume" in query:
        change_volume(up=False)
        return "Volume decreased."

    elif "mute" in query:
        mute_volume(True)
        return "Volume muted."

    elif "unmute" in query:
        mute_volume(False)
        return "Volume unmuted."

    elif "set volume to" in query:
        match = re.search(r"set volume to (\d+)", query)
        if match:
            percent = int(match.group(1))
            set_volume_level(percent)
            return f"Volume set to {percent}%."

    # 💡 Brightness
    elif "increase brightness" in query:
        change_brightness(up=True)
        return "Brightness increased."

    elif "decrease brightness" in query:
        change_brightness(up=False)
        return "Brightness decreased."

    elif "set brightness to" in query:
        match = re.search(r"set brightness to (\d+)", query)
        if match:
            percent = int(match.group(1))
            set_brightness(percent)
            return f"Brightness set to {percent}%."

    # 📄 Recent Files
    elif "recent files" in query or "files used today" in query:
        return get_recent_files(within_hours=24)

    elif "files modified in the last hour" in query:
        return get_recent_files(within_hours=1)

    # 🔐 System Commands
    elif "lock system" in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "System locked."

    elif "shutdown" in query:
        os.system("shutdown /s /t 1")
        return "Shutting down the system."

    elif "restart" in query:
        os.system("shutdown /r /t 1")
        return "Restarting the system."

    elif "change system password" in query:
        from core.permissions import change_password_gui
        change_password_gui()
        return "Changing password."

    # 🧠 Memory
    elif "show my history" in query or "assistant memory" in query:
        from core.logger import read_log
        return read_log()

    # 🔗 Internet Tools
    # Calculator
    if "calculate" in query or "what is" in query:
        result = evaluate_expression(query)
        if result:
            return result

    # Wikipedia
    # TODO: ("who is", "what is")
    if any(kw in query for kw in ["tell me about", "who is", "what is"]):
        result = fetch_wikipedia_summary(query)
        if result:
            return result

    # Weather
    # TODO: Location error
    if "weather in" in query:
        result = get_weather_info(query)
        if result:
            return result

    # ❌ Unknown command
    return None
