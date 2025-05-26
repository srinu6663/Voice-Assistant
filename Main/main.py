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
    get_news,
)
from functions import takeCommand, speak, wishMe
from reminder import handle_reminder
from commands import open_app_by_name, open_url 

import speech_recognition as sr
import threading


hotword_active = True  # Global flag 
activation_lock = threading.Lock()

def start_hotword_listener(callback_func, hotword="hey jarvis"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    def hotword_callback(rec, audio):
        try:
            trigger = rec.recognize_google(audio).lower()
            if hotword in trigger:
                if activation_lock.acquire(blocking=False):
                    try:
                        callback_func()
                    finally:
                        activation_lock.release()
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"Hotword error: {e}")

    recognizer.listen_in_background(mic, hotword_callback)

def main():
    speak("Loading your AI personal assistant E-On")
    print("Loading your AI personal assistant E-On")
    wishMe()

    # Start hotword listener in background
    threading.Thread(target=start_hotword_listener, args=(activate_assistant, "hey jarvis"), daemon=True).start()

    while True:
        print("\n🟢 Press 'Ctrl + Space' or Say 'hey E-On' to activate...")
        keyboard.wait("ctrl+space")

        # Use lock to prevent overlap
        if activation_lock.acquire(blocking=False):  # Only allow if not already active
            try:
                activate_assistant()
            finally:
                activation_lock.release()



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
        handle_wolfram_or_chatbot()

    elif "log off" in statement or "sign out" in statement:
        handle_logoff()

    elif "notify me" in statement or "remind me" in statement:
        handle_reminder()
        
    elif "news" in statement:
        get_news(statement)

    else:
        handle_chatbot_fallback(statement)


if __name__ == '__main__':
    main()
