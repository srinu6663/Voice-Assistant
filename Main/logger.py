import csv
import os
from datetime import datetime

# Create the logs folder and file if not exist
LOG_FILE = "logs/feature_logs.csv"
os.makedirs("logs", exist_ok=True)

# Ensure headers are written only once
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Feature", "ExecutionTime(s)", "Status"])

def log_performance(feature_name: str, execution_time: float, success: bool = True):
    """Logs the execution time (already calculated) and status of a feature."""
    status = "Success" if success else "Failed"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, feature_name, round(execution_time, 2), status])
