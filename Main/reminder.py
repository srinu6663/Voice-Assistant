import dateparser
from datetime import datetime, timedelta
import pyttsx3
from plyer import notification
import time
import threading
import speech_recognition as sr
import re

reminders = []


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()


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

def add_reminder(title, message, delay_minutes):
    trigger_time = datetime.now() + timedelta(minutes=delay_minutes)
    reminders.append((trigger_time, title, message))
    print(f"Reminder set for {trigger_time.strftime('%H:%M:%S')} - {title}: {message}")

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def reminder_checker():
    while True:
        current_time = datetime.now()
        for reminder in reminders[:]:
            trigger_time, title, message = reminder
            if current_time >= trigger_time:
                show_notification(title, message)
                reminders.remove(reminder)
        time.sleep(5)

# Background thread for checking reminders
threading.Thread(target=reminder_checker, daemon=True).start()


def extract_time_phrase(text):
    # Try to extract the time-related part from the command
    match = re.search(r'\b(in .*|at .*|tomorrow.*)', text)
    return match.group(0) if match else None

def handle_reminder():
    speak("What should I remind you, and when?")
    full_input = takeCommand().lower()
    print(f"Full Input Received: {full_input}")

    time_phrase = extract_time_phrase(full_input)
    print(f"Extracted Time Phrase: {time_phrase}")  # Debug print

    if not time_phrase:
        speak("I couldn't find a time in your message. Please try again.")
        return

    reminder_time = dateparser.parse(time_phrase)
    if not reminder_time:
        speak("I couldn't understand the time. Please try again.")
        return

    now = datetime.now()
    delay = (reminder_time - now).total_seconds()

    if delay <= 0:
        speak("That time is in the past. Please provide a future time.")
        return

    delay_minutes = delay / 60
    message = full_input.replace(time_phrase, "").strip()
    if not message:
        message = "Reminder"

    add_reminder("Reminder", message, delay_minutes)
    speak(f"Reminder set in {int(delay_minutes)} minutes for: {message}.")

