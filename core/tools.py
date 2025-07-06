import os
import subprocess
import platform
import webbrowser
from googletrans import Translator


APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vsc": "D:\\College\\App\\Microsoft VS Code\\Code.exe"
    # Add more apps as needed
}


def launch_app(app_name):
    app_name = app_name.lower()
    path = APP_PATHS.get(app_name)

    if not path:
        return f"❌ Unknown app: {app_name}"

    try:
        if platform.system() == "Windows":
            subprocess.Popen(path)
        else:
            os.system(path)
        return f"🚀 Launching {app_name.title()}"
    except Exception as e:
        return f"❌ Failed to launch {app_name}: {e}"


def search_web(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"🔍 Searching Google for: {query}"
    except Exception:
        return "❌ Failed to open browser."


def translate_text(text, target_lang="en"):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return f"🗣️ Translated to {target_lang}: {translated.text}"
    except Exception:
        return "❌ Translation failed."
