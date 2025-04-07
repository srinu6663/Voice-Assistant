import pywhatkit as kit
import wikipedia
import requests
import datetime
import subprocess
from ecapture import ecapture as ec
import datetime
import wikipedia
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import openai
from commands import set_brightness_level, get_current_brightness, set_volume_level, get_current_volume , open_app_by_name
from memory import store_chat
from reminder import add_reminder
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import math
import pyttsx3
import datetime
import os
import wolframalpha
from logger import log_performance
import time




import speech_recognition as sr

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


print('Loading your AI personal assistant - E-On')

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



def play_youtube(song_name, speak):
    try:
        start_time = time.time()
        print(f"🎥 Playing {song_name} on YouTube...")
        speak(f"Playing {song_name} on YouTube.")
        kit.playonyt(song_name)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("YouTube Play", execution_time, success=True)
    except Exception as e:
        print(f"Error playing YouTube: {e}")
        speak("Sorry, I couldn't play that song on YouTube.")
        log_performance("YouTube Play", 0.0, success=False)


def handle_wikipedia(statement):
    try:
        start_time = time.time()
        speak('Searching Wikipedia...')
        query = statement.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        store_chat(statement, results)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Wikipedia Search", execution_time, success=True)
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't find that on Wikipedia.")
        log_performance("Wikipedia Search", 0.0, success=False)

def handle_youtube():
    try:
        start_time = time.time()
        speak("Which song do you want to play?")
        song = takeCommand()
        play_youtube(song, speak)
        response = f"Playing {song} on YouTube"
        store_chat(f"Play YouTube: {song}", response)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("YouTube Play", execution_time, success=True)
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't play that song on YouTube.")
        log_performance("YouTube Play", 0.0, success=False)

# def handle_open_url(statement):
#     try:
#         start_time = time.time()
#         open_url(statement, speak)
#         store_chat(statement, "Opened website")
#         end_time = time.time()
#         execution_time = end_time - start_time
#         log_performance("Open URL", execution_time, success=True)
#     except Exception as e:
#         print(f"Error: {e}")
#         speak("Sorry, I couldn't open that URL.")
#         log_performance("Open URL", 0.0, success=False)


def handle_brightness(statement):
    try:
        start_time = time.time()
        if "set" in statement:
            speak("What brightness level do you want?")
            level = int(takeCommand().replace("%", ""))
            set_brightness_level(level, speak)
        else:
            get_current_brightness(speak)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Brightness Control", execution_time, success=True)
    except Exception as e:
        print(f"Brightness Error: {e}")
        speak("Sorry, I couldn't change the brightness.")
        log_performance("Brightness Control", 0.0, success=False)

def handle_volume(statement):
    try:
        start_time = time.time()
        if "set" in statement:
            speak("What volume level do you want?")
            level = int(takeCommand().replace("%", ""))
            set_volume_level(level, speak)
        else:
            get_current_volume(speak)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Volume Control", execution_time, success=True)
    except Exception as e:
        print(f"Volume Error: {e}")
        speak("Sorry, I couldn't change the volume.")
        log_performance("Volume Control", 0.0, success=False)

def handle_open_app(statement):
    try:
        start_time = time.time()
        app_name = statement.replace("open", "").strip()
        open_app_by_name(app_name, speak)
        store_chat(statement, f"Opened app: {app_name}")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Open App", execution_time, success=True)
    except Exception as e:
        print(f"Open App Error: {e}")
        speak("Sorry, I couldn't open that app.")
        log_performance("Open App", 0.0, success=False)

def handle_weather():
    try:
        start_time = time.time()
        log_performance("Weather Report", start_time, success=True)
        api_key = "8ef61edcf1c576d65d836254e11ea420"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        speak("What's the city name?")
        city_name = takeCommand()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response_data = requests.get(complete_url).json()

        if response_data["cod"] != "404":
            y = response_data["main"]
            temp_celsius = round(y["temp"] - 273.15, 2)
            humidity = y["humidity"]
            description = response_data["weather"][0]["description"]
            weather_report = f"The weather in {city_name} is {description}. Temperature: {temp_celsius}°C, Humidity: {humidity}%."
        else:
            weather_report = "City not found"

        speak(weather_report)
        print(weather_report)
        store_chat(city_name, weather_report)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Weather Report", execution_time, success=True)
    except Exception as e:
        print(f"Weather Error: {e}")
        speak("Sorry, I couldn't fetch the weather report.")
        log_performance("Weather Report", 0.0, success=False)

def handle_time():
    try:
        start_time = time.time()
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time_str}")
        print(f"The time is {time_str}")
        store_chat("time", time_str)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Time Report", execution_time, success=True)
    except Exception as e:
        print(f"Time Error: {e}")
        speak("Sorry, I couldn't fetch the time.")
        log_performance("Time Report", 0.0, success=False)

def handle_identity():
    try:
        start_time = time.time()
        info = (
            'I am G-One version 1.0, your personal assistant. '
            'I can perform minor tasks like opening websites, predicting the time, taking photos, '
            'searching Wikipedia, providing weather updates, fetching news, and answering questions!'
        )
        speak(info)
        print(info)
        store_chat("identity", info)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Identity Report", execution_time, success=True)
    except Exception as e:
        print(f"Identity Error: {e}")
        speak("Sorry, I couldn't provide my identity.")
        log_performance("Identity Report", 0.0, success=False)

def handle_camera():
    try:
        start_time = time.time()
        ec.capture(0, "robo camera", "img.jpg")
        speak("Captured a photo")
        store_chat("camera", "Captured a photo")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Camera Report", execution_time, success=True)
    except Exception as e:
        print(f"Camera Error: {e}")
        speak("Sorry, I couldn't capture a photo.")
        log_performance("Camera Report", 0.0, success=False)


def handle_wolfram_or_chatbot():
    """Handles WolframAlpha queries and falls back to a chatbot if needed."""
    try:
        start_time = time.time()
        speak("What do you want to ask? You can also type if you'd prefer.")
        try:
            question = takeCommand(timeout=3)
            if not question:
                raise Exception("No speech detected")
        except:
            speak("I didn't hear anything. Please type your question.")
            question = input("Type your question: ")

        if question:
            app_id = "62R7KQ-5VLLXK8LTW"
            client = wolframalpha.Client(app_id)
            try:
                res = client.query(question)
                if res['@success'] == 'true' and hasattr(res, 'results'):
                    try:
                        answer = next(res.results).text
                        if "(data not available)" in answer.lower() or not answer.strip():
                            raise ValueError("No useful data")
                        speak(answer)
                        print(answer)
                        store_chat(question, answer)
                    except (StopIteration, ValueError):
                        speak("WolframAlpha didn't help. Asking AI...")
                        detailed, summary = get_chatbot_response(question)
                        speak(summary)
                        print(detailed)
                        store_chat(question, detailed)
                else:
                    speak("WolframAlpha failed. Asking AI...")
                    detailed, summary = get_chatbot_response(question)
                    speak(summary)
                    print(detailed)
                    store_chat(question, detailed)
            except Exception as e:
                speak("Error reaching WolframAlpha. Asking AI...")
                detailed, summary = get_chatbot_response(question)
                speak(summary)
                print(detailed)
                store_chat(question, detailed)
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("WolframAlpha Query", execution_time, success=True)
    except Exception as e:
        print(f"WolframAlpha Error: {e}")
        speak("Sorry, I couldn't process your request.")
        log_performance("WolframAlpha Query", 0.0, success=False)

def handle_logoff():
    try:
        start_time = time.time()
        speak("Logging off in 10 seconds. Save your work.")
        subprocess.call(["shutdown", "/l"])
        store_chat("logoff", "System logging off")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Log Off", execution_time, success=True)
    except Exception as e:
        print(f"Error logging off: {e}")
        speak("Sorry, I couldn't log off the system.")
        log_performance("Log Off", 0.0, success=False)


def handle_reminder():
    try:
        start_time = time.time()
        speak("What should I remind you about?")
        title = takeCommand()
        speak("When should I remind you? (in minutes)")
        minutes = takeCommand()
        add_reminder(title, "Reminder alert", int(minutes))
        speak("Reminder set successfully")
        store_chat("reminder", f"Reminder: {title} in {minutes} minutes")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Set Reminder", execution_time, success=True)
    except Exception as e:
        print(f"Reminder Error: {e}")
        speak("Sorry, I couldn't set the reminder.")
        log_performance("Set Reminder", 0.0, success=False)

def handle_chatbot_fallback(statement):
    detailed, summary = get_chatbot_response(statement)
    speak(summary)
    print(f"🤖 Chatbot: {detailed}")
    store_chat(statement, detailed)



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
