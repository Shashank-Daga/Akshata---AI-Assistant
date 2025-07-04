import speech_recognition as sr


def get_user_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")

            query = recognizer.recognize_google(audio)
            return query.lower()

        except sr.WaitTimeoutError:
            print("No Speech Detected.")
            return "I didn't hear anything"

        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return "Sorry, I couldn't understand."

        except sr.RequestError:
            print("Could not request results")
            return "Internet issue or service down."

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while listening."
