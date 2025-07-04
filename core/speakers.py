import pyttsx3

# Initialize the TTS engine once
engine = pyttsx3.init()


# Optional: Adjust voice, rate, volume
def setup_voice():
    voices = engine.getProperty('voices')
    # For female voice, pick index 1 (usually female on Windows)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Max volume


# Call this once at import
setup_voice()


def speak(text):
    print(f"🗣️ Speaking: {text}")
    engine.say(text)
    engine.runAndWait()
