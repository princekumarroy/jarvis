import speech_recognition as sr
import webbrowser
import pyttsx3
from google import genai
from dotenv import load_dotenv
import os


# Gemini setup
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


# Speech setup
recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "system_instruction": (
                    "You are Jarvis, a helpful and concise voice assistant. "
                    "Give short answers suitable for speech."
                )
            }
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return "Sorry sir, I am facing some technical issues."


if __name__ == "__main__":

    speak("I am ready to begin, boss.")

    # Listen for the wake word
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)

        if "jarvis" in command:

            speak("Yes sir, I am listening.")

            # Listen for the actual command
            with sr.Microphone() as source:
                print("Listening for your command...")

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            command = recognizer.recognize_google(audio).lower()

            print("Command:", command)

            if "who are you" in command:

                speak("I am Jarvis, your personal assistant.")

            elif "open google" in command:

                speak("Opening Google.")
                webbrowser.open("https://www.google.com")

            elif "open youtube" in command:

                speak("Opening YouTube.")
                webbrowser.open("https://www.youtube.com")

            elif "favourite song" in command:

                speak("playing man ki lagan")
                webbrowser.open("https://youtu.be/lrkaKvhRnEI?si=eJZaw5HUGhUyj9zX")

            else:

                response = ask_gemini(command)
                print("Jarvis:", response)
                speak(response)

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand.")

    except sr.RequestError as e:

        print("Speech Recognition service error:", e)

    except sr.WaitTimeoutError:

        print("I didn't hear anything.")