import webbrowser
from googletrans import Translator


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
