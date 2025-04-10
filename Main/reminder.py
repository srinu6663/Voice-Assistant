import dateparser
from datetime import datetime, timedelta
from plyer import notification
import time
import threading
import re
from logger import log_performance
from functions import takeCommand, speak

reminders = []

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
    try:
        speak("What should I remind you, and when?")
        full_input = takeCommand().lower()
        print(f"Full Input Received: {full_input}")

        time_phrase = extract_time_phrase(full_input)
        print(f"Extracted Time Phrase: {time_phrase}")  # Debug print

        start_time = time.time()

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
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        log_performance("Set reminder", execution_time, success=True)
    except Exception as e:
        log_performance("Set reminder", execution_time, success=False)
