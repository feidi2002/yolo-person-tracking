# src/zone_logger.py
import os
import cv2
from datetime import datetime

LOG_FILE = "output/alert_log.txt"
CAPTURE_DIR = "output/captures"

os.makedirs(CAPTURE_DIR, exist_ok=True)

def log_event(event_type, box, frame):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"[{timestamp}] {event_type} at {box}\n"
    with open(LOG_FILE, "a") as f:
        f.write(message)

    # Sauvegarder image
    filename = f"{event_type}_{timestamp.replace(':', '-').replace(' ', '_')}.jpg"
    path = os.path.join(CAPTURE_DIR, filename)
    cv2.imwrite(path, frame)