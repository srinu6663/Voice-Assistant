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

import keyboard
from features import (
    handle_wikipedia,
    handle_youtube,
    handle_weather,
    handle_brightness,
    handle_volume,
    handle_time,
    handle_identity,
    handle_camera,
    handle_wolfram_or_chatbot,
    handle_logoff,
    handle_reminder,
    handle_chatbot_fallback,
    takeCommand,
    speak,
    wishMe
)
from commands import open_app_by_name, open_url  # ✅ Import the URL handling function

import speech_recognition as sr
import threading

def start_hotword_listener(hotword="hey jarvis"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    def callback(rec, audio):
        try:
            trigger = rec.recognize_google(audio).lower()
            if hotword in trigger:
                # print("🟢 Hotword detected!")
                activate_assistant()
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"Hotword error: {e}")

    recognizer.listen_in_background(mic, callback)




def main():
    speak("Loading your AI personal assistant E-On")
    wishMe()

    # 🔊 Start hotword listener
    start_hotword_listener(activate_assistant, hotword="E-On")

    while True:
        print("\n🟢 Press 'Ctrl + Space' or Say 'hey E-On' to activate...")
        keyboard.wait("ctrl+space")
        activate_assistant()



def activate_assistant():
    speak("Tell me, how can I help you?")
    print("Tell me, how can I help you?")
    statement = takeCommand().lower()
    if statement == "none":
        return

    if any(word in statement for word in ["goodbye", "bye", "stop"]):
        speak("Your personal assistant E-On is shutting down. Goodbye!")
        print("Your personal assistant E-On is shutting down. Goodbye!")
        exit()

    elif 'wikipedia' in statement:
        handle_wikipedia(statement)

    elif "play" in statement and "youtube" in statement:
        handle_youtube()

    elif 'open' in statement and "website" in statement:
        statement = statement.replace("open", "").replace("website", "").strip()
        open_url(statement)

    elif "set brightness" in statement or "what is my brightness" in statement:
        handle_brightness(statement)

    elif "set volume" in statement or "what is my volume" in statement:
        handle_volume(statement)

    elif "open" in statement and "app" in statement:
        app_name = statement.replace("open", "").replace("app", "").strip()
        open_app_by_name(app_name, speak)

    elif "weather" in statement:
        handle_weather()

    elif 'time' in statement:
        handle_time()

    elif 'who are you' in statement or 'what can you do' in statement:
        handle_identity()

    elif "camera" in statement or "take a photo" in statement:
        handle_camera()

    elif any(word in statement for word in ["calculate", "compute", "solve", "define", "lookup", "explain", "analyze", "query"]):
        handle_wolfram_or_chatbot(statement)

    elif "log off" in statement or "sign out" in statement:
        handle_logoff()

    elif "notify me" in statement or "remind me" in statement:
        handle_reminder()

    else:
        handle_chatbot_fallback(statement)


if __name__ == '__main__':
    main()
