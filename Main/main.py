# import speech_recognition as sr
# import pyttsx3
# import datetime
# import wikipedia
# import os
# import time
# import subprocess
# from ecapture import ecapture as ec
# import wolframalpha
# import requests
# from commands import open_url  # ✅ Import the URL handling function

# print('Loading your AI personal assistant - G One')

# # ✅ Initialize Text-to-Speech Engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# # ✅ Speak Function
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # ✅ Greeting Function
# def wishMe():
#     hour = datetime.datetime.now().hour
#     if hour >= 0 and hour < 12:
#         speak("Hello, Good Morning")
#     elif hour >= 12 and hour < 18:
#         speak("Hello, Good Afternoon")
#     else:
#         speak("Hello, Good Evening")

# # ✅ Take Command from Microphone
# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)

#         try:
#             statement = r.recognize_google(audio, language='en-in')
#             print(f"user said: {statement}\n")

#         except Exception as e:
#             speak("Pardon me, please say that again")
#             return "None"
#         return statement.lower()

# # ✅ Initialize Assistant
# speak("Loading your AI personal assistant G-One")
# wishMe()

# if __name__ == '__main__':
#     while True:
#         speak("Tell me how can I help you now?")
#         statement = takeCommand()

#         if statement == "none":
#             continue

#         # ✅ Exit Commands
#         if "goodbye" in statement or "bye" in statement or "stop" in statement:
#             speak('Your personal assistant G-One is shutting down. Goodbye!')
#             print('Your personal assistant G-One is shutting down. Goodbye!')
#             break

#         # ✅ Wikipedia Search
#         elif 'wikipedia' in statement:
#             speak('Searching Wikipedia...')
#             statement = statement.replace("wikipedia", "")
#             results = wikipedia.summary(statement, sentences=3)
#             speak("According to Wikipedia")
#             print(results)
#             speak(results)

#         # ✅ Open URL (using the separate function)
#         elif 'open' in statement:
#             open_url(statement, speak)

#         # ✅ Weather Information
#         elif "weather" in statement:
#             api_key = "8ef61edcf1c576d65d836254e11ea420"
#             base_url = "https://api.openweathermap.org/data/2.5/weather?"
#             speak("What's the city name?")
#             city_name = takeCommand()
#             complete_url = base_url + "appid=" + api_key + "&q=" + city_name
#             response = requests.get(complete_url)
#             x = response.json()

#             if x["cod"] != "404":
#                 y = x["main"]
#                 current_temperature = y["temp"]
#                 current_humidity = y["humidity"]
#                 z = x["weather"]
#                 weather_description = z[0]["description"]
#                 speak(f"Temperature in Kelvin: {current_temperature}, Humidity: {current_humidity}%, Description: {weather_description}")
#                 print(f"Temperature: {current_temperature}K\nHumidity: {current_humidity}%\nDescription: {weather_description}")
#             else:
#                 speak("City Not Found")

#         # ✅ Time
#         elif 'time' in statement:
#             strTime = datetime.datetime.now().strftime("%H:%M:%S")
#             speak(f"The time is {strTime}")

#         # ✅ Introduction
#         elif 'who are you' in statement or 'what can you do' in statement:
#             speak('I am G-One version 1.0, your personal assistant. I can perform minor tasks like opening websites, '
#                 'predicting the time, taking photos, searching Wikipedia, providing weather updates, '
#                 'fetching news, and answering computational or geographical questions!')

#         # ✅ Camera
#         elif "camera" in statement or "take a photo" in statement:
#             ec.capture(0, "robo camera", "img.jpg")

#         # ✅ WolframAlpha Queries
#         elif 'ask' in statement:
#             speak('I can answer computational and geographical questions. What do you want to ask?')
#             question = takeCommand()
#             app_id = "62R7KQ-5VLLXK8LTW"
#             client = wolframalpha.Client(app_id)
#             res = client.query(question)
#             answer = next(res.results).text
#             speak(answer)
#             print(answer)

#         # ✅ System Log Off
#         elif "log off" in statement or "sign out" in statement:
#             speak("Ok, your PC will log off in 10 seconds. Make sure you exit all applications.")
#             subprocess.call(["shutdown", "/l"])

#         time.sleep(3)

import pyttsx3
import datetime
import wikipedia
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import keyboard
import openai
from commands import open_url, set_brightness_level, get_current_brightness, set_volume_level, get_current_volume, open_app
from memory import store_chat
from reminder import add_reminder
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import math
from features import play_youtube

import speech_recognition as sr

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


print('Loading your AI personal assistant - E On')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")


def takeCommand(timeout=5):
    """Fast and accurate voice recognition using Google Speech API."""
    
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening...")

        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Google Speech API is unavailable.")

    return ""


def main():
    speak("Loading your AI personal assistant E-On")
    wishMe()


    while True:
        print("\n🟢Press 'Ctrl + Space' to activate...")

        keyboard.wait("ctrl+space")

        speak("Tell me, how can I help you?")
        statement = takeCommand()

        if statement == "none":
            continue

        if "goodbye" in statement or "bye" in statement or "stop" in statement:
            speak('Your personal assistant G-One is shutting down. Goodbye!')
            print('Your personal assistant G-One is shutting down. Goodbye!')
            store_chat(statement, "Goodbye!")
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            response = results

        elif "play" in statement and "youtube" in statement:
            speak("Which song do you want to play?")
            song = takeCommand()
            play_youtube(song, speak)
            response = f"Playing {song} on YouTube"

        elif 'open' in statement:
            open_url(statement, speak)

        elif "set brightness" in statement:
            try:
                speak("What brightness level do you want?")
                level = int(takeCommand().replace("%", ""))
                set_brightness_level(level,speak)
            except Exception as e:
                print(f"Brightness Error: {e}")

        elif "what is my brightness" in statement:
            get_current_brightness(speak)

        elif "set volume" in statement:
            try:
                speak("What volume level do you want?")
                level = int(takeCommand().replace("%", ""))
                set_volume_level(level,speak)
            except Exception as e:
                print(f"Volume Error: {e}")

        elif "what is my volume" in statement:
            get_current_volume(speak)

        elif "open" in statement:
            try:
                app_name = statement.replace("open", "").strip()
                open_app(app_name,speak)
            except Exception as e:
                print(f"Open App Error: {e}")
            
        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response_data = requests.get(complete_url).json()

            if response_data["cod"] != "404":
                y = response_data["main"]

                current_temperature = round(y["temp"] - 273.15, 2)
                current_humidity = y["humidity"]
                z = response_data["weather"]
                weather_description = z[0]["description"]

                weather_report = (
                    f"The weather in {city_name} is {weather_description}. "
                    f"Temperature: {current_temperature}°C, "
                    f"Humidity: {current_humidity}%."
                )

                speak(weather_report)
                print(weather_report)
                response = weather_report

            else:
                response = "City not found"
                speak(response)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")
            response = f"The time is {strTime}"

        elif 'who are you' in statement or 'what can you do' in statement:
            print(info)
            info = (
                'I am G-One version 1.0, your personal assistant. '
                'I can perform minor tasks like opening websites, '
                'predicting the time, taking photos, searching Wikipedia, '
                'providing weather updates, fetching news, and answering questions!'
            )
            speak(info)
            response = info

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")
            response = "Captured a photo"

        elif any(word in statement for word in ["calculate", "compute", "solve", "define", "lookup", "explain", "analyze", "query"]):
            speak('I can answer computational and geographical questions. What do you want to ask?')
            question = takeCommand()
            app_id = "62R7KQ-5VLLXK8LTW"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
            response = answer

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit all applications.")
            subprocess.call(["shutdown", "/l"])
            response = "System logging off"

        elif "notify me" in statement:
                try:
                    speak("What should I remind you about?")
                    reminder_title = takeCommand()
                    speak("When should I remind you? (in minutes)")
                    reminder_time = takeCommand()
                    add_reminder(reminder_title, "Reminder alert", int(reminder_time))
                    speak("Reminder set successfully")
                except Exception as e:
                    print(f"Reminder Error: {e}")
        else:
            detailed_response, summary = get_chatbot_response(statement)
            print(f"🤖 Chatbot: {detailed_response}")
            speak(summary)

            store_chat(statement, detailed_response)

        time.sleep(1)


openai.api_key = "bf54edfec7746118fdbd36003e3f450fb8f5fef9a9464a527b097714ca01579b"
openai.api_base = "https://api.together.xyz/v1"

def get_chatbot_response(prompt):
    """Get a detailed response from Together AI and return detailed + summarized version"""
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide detailed and factual answers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        detailed_response = response['choices'][0]['message']['content'].strip()

        summary = generate_summary(detailed_response)

        return detailed_response, summary

    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble responding right now.", "I'm having trouble responding."

def generate_summary(text, ratio=0.2):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        sentence_count = len(parser.document.sentences)
        
        summary_length = max(1, math.ceil(sentence_count * ratio))
        
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, summary_length)

        summary_text = " ".join(str(sentence) for sentence in summary)

        if len(summary_text) < 20:
            return text[:300]

        return summary_text

    except Exception:
        return text[:300]



if __name__ == '__main__':
    main()
