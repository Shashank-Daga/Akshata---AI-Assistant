import speech_recognition as sr


def get_user_input(timeout=5, phrase_time_limit=8):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🔊 Adjusting for ambient noise...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("🧠 Recognizing...")

            query = recognizer.recognize_google(audio)
            print(f"✅ Recognized: {query}")
            return query.lower()

        except sr.WaitTimeoutError:
            print("❌ No speech detected (timeout).")
            return "I didn't hear anything"

        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
            return "Sorry, I couldn't understand."

        except sr.RequestError:
            print("❌ Speech recognition service unavailable.")
            return "Internet issue or service down."

        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return "An error occurred while listening."
