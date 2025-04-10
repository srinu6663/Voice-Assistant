import subprocess
import time
import webbrowser
import requests
import pyttsx3
from screen_brightness_control import set_brightness, get_brightness
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
from logger import log_performance
from functions import speak


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def open_url(query, speak=None):
    # Clean the query
    query = query.strip().lower()

    # Add protocol if not present
    if not query.startswith("http"):
        # Try forming a smart URL
        domain_extensions = [".com", ".in", ".org", ".net", ".edu"]
        for ext in domain_extensions:
            url = f"https://{query.replace(' ', '')}{ext}"
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    webbrowser.open_new_tab(url)
                    if speak:
                        speak(f"Opening {url}")
                    print(f"🌍 Opening: {url}")
                    return
            except:
                continue

    # If nothing matched, fall back to Google Search
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)
    if speak:
        speak(f"I couldn't find the website. Searching Google for {query}")
    print(f"🔍 Searching Google for: {query}")

def set_brightness_level(level):
    try:
        start_time = time.time()
        set_brightness(level)
        speak(f"Brightness set to {level} percent")
        end_time = time.time()
        execution_time =end_time - start_time
        log_performance("Brightness Adjustment", execution_time, success=True)
    except Exception as e:
        print(f"Brightness Error: {e}")
        speak("I couldn't adjust the brightness. Please try again.")
        log_performance("Brightness Adjustment", 0.0, success=False)

def get_current_brightness():
    try:
        start_time = time.time()
        brightness = get_brightness()
        speak(f"Current brightness is {brightness[0]} percent")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Brightness Read", execution_time, success=True)
    except Exception as e:
        print(f"Brightness Read Error: {e}")
        speak("I couldn't read the brightness level. Please try again.")
        log_performance("Brightness Read", 0.0, success=False)

# 🔊 Volume Control
def set_volume_level(level):
    try:
        start_time = time.time()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level} percent")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Volume Adjustment", execution_time, success=True)
    except Exception as e:
        print(f"Volume Error: {e}")
        speak("I couldn't adjust the volume. Please try again.")
        log_performance("Volume Adjustment", 0.0, success=False)

def get_current_volume():
    try:
        start_time = time.time()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
        speak(f"Current volume is {current_volume} percent")
        end_time = time.time()
        execution_time = end_time - start_time
        log_performance("Volume Read", execution_time, success=True)
    except Exception as e:
        print(f"Volume Read Error: {e}")
        speak("I couldn't read the volume level. Please try again.")
        log_performance("Volume Read", 0.0, success=False)



import json
import subprocess

with open("app_paths.json", "r") as f:
    app_paths = json.load(f)

def open_app_by_name(app_name, speak):
    app_key = app_name.lower().strip()
    if app_key in app_paths:
        start_time = time.time()
        try:
            subprocess.Popen(app_paths[app_key])
            speak(f"Opening {app_name}")
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            log_performance("Open Application", execution_time, success=True)
        except Exception as e:
            print(f"Error opening app: {e}")
            speak("Sorry, I couldn't open the application.")
            log_performance("Open Application", 0.0, success=False)
    else:
        print(f"App '{app_name}' not found in known paths.")
        speak("I couldn't find that application. Please try another one.")
        log_performance("Open Application", 0.0, success=False)


