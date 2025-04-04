import subprocess
import webbrowser
import re
from screen_brightness_control import set_brightness, get_brightness
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes


saved_websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "news": "https://timesofindia.indiatimes.com/home/headlines"
}


def is_valid_url(query):
    """Check if the query contains a valid domain (like 'google.com')."""
    return bool(re.search(r"\.[a-z]{2,}$", query)) 

def open_url(query, speak):
    """
    Opens a URL or website based on the command.
    
    :param query: The spoken command
    :param speak: The speak function reference for feedback
    """
    query = query.replace("open", "").strip()

    print(f"🔍 Processing query: {query}")

    if query in saved_websites:
        web_url = saved_websites[query]
        speak(f"Opening {query}")
        print(f"🌍 Opening website: {web_url}")
        webbrowser.open(web_url)

    elif is_valid_url(query):
        web_url = f"https://{query}"
        speak(f"Opening {query}")
        print(f"🌍 Opening website: {web_url}")
        webbrowser.open(web_url)

    else:
        web_url = f"https://{query}.com"
        speak(f"Opening {query}")
        print(f"🌍 Trying website: {web_url}")
        webbrowser.open(web_url)

def set_brightness_level(level,speak):
    try:
        set_brightness(level)
        speak(f"Brightness set to {level} percent")
    except Exception as e:
        print(f"Brightness Error: {e}")

def get_current_brightness(speak):
    try:
        brightness = get_brightness()
        speak(f"Current brightness is {brightness[0]} percent")
    except Exception as e:
        print(f"Brightness Read Error: {e}")

# 🔊 Volume Control
def set_volume_level(level,speak):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level} percent")
    except Exception as e:
        print(f"Volume Error: {e}")

def get_current_volume(speak):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
        speak(f"Current volume is {current_volume} percent")
    except Exception as e:
        print(f"Volume Read Error: {e}")

def open_app(app_name,speak):
    try:
        # Check if the app exists
        result = subprocess.run(f'where {app_name}', shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            speak(f"Opening {app_name}")
            subprocess.Popen(app_name, shell=True)
        else:
            speak("Application not found. Try specifying a different name.")
    except Exception as e:
        print(f"Open App Error: {e}")
        speak("I couldn't open the application.")
