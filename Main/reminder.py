from plyer import notification
from datetime import datetime, timedelta
import time
import threading

reminders = []

def add_reminder(title, message, delay_minutes):
    """Add a reminder to the list."""
    trigger_time = datetime.now() + timedelta(minutes=delay_minutes)
    reminders.append((trigger_time, title, message))
    print(f"Reminder set for {trigger_time.strftime('%H:%M:%S')} - {title}: {message}")

def show_notification(title, message):
    """Display a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def reminder_checker():
    """Continuously check if any reminder time has passed."""
    while True:
        current_time = datetime.now()
        for reminder in reminders[:]:
            trigger_time, title, message = reminder
            if current_time >= trigger_time:
                show_notification(title, message)
                reminders.remove(reminder)
        time.sleep(5)

threading.Thread(target=reminder_checker, daemon=True).start()
