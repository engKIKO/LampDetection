from datetime import datetime

# Custom night time range
NIGHT_START = 18  # 6 PM
NIGHT_END = 6     # 6 AM

def is_night(current_hour=None):
    if current_hour is None:
        current_hour = datetime.now().hour

    return current_hour >= NIGHT_START or current_hour < NIGHT_END

def log_broken_lamp(lamp_id, label, log_path="brokenLamps.log"):
    with open(log_path, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Lamp {lamp_id} is OFF during night. Status: {label}\n")
