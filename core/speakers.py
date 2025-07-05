import pyttsx3

# TTS engine initialization
engine = pyttsx3.init()

# Global flag (could come from config later)
is_tts_enabled = True


# Optional: Adjust voice, rate, volume
def setup_voice():
    try:
        voices = engine.getProperty('voices')

        # Attempt to set a female voice
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            engine.setProperty('voice', voices[0].id)  # Default to first

        engine.setProperty('rate', 180)    # Speed of speech
        engine.setProperty('volume', 1.0)  # Max volume

    except Exception as e:
        print(f"TTS setup error: {e}")


# Speak text
def speak(text):
    if not is_tts_enabled:
        print(f"[Muted] {text}")
        return

    try:
        print(f"🗣️ Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")


# Initialize on import
setup_voice()
