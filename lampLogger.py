import os
from datetime import datetime
import json
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

bucket = os.getenv("INFLUX_BUCKET")
org = os.getenv("INFLUX_ORG")
token = os.getenv("INFLUX_TOKEN")
url = os.getenv("INFLUX_URL")
NIGHT_START = os.getenv("NIGHT_START")
NIGHT_END = os.getenv("NIGHT_END")

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)




def time_is_night(current_hour=None):
    if current_hour is None:
        current_hour = datetime.now().hour

    return current_hour >= NIGHT_START or current_hour < NIGHT_END

def log_broken_lamp(lamp_id, label, status="broken",reason="majority 'off' detections during night", log_path="brokenLamps.log"):
    with open(log_path, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Lamp {lamp_id} is OFF during night. Cam_detection: {label} status:{status} Reason:{reason}\n")
        # return f"[{timestamp}] Lamp {lamp_id} is OFF during night. Cam_detection: {label} status:{status} Reason:{reason}\n"
        return log_json(lamp_id=lamp_id,label=label,status=status,reason=reason)

def log_json(lamp_id, label, status="broken",reason="majority 'off' detections during night"):
    jsonString = {
        "Lamp_id" :lamp_id,
        "lablel" : label,
        "status" :status,
        "reson" :reason,
        "time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return json.dumps(jsonString)

def log_lamp_status(lamp_id,label, status, confidence,reason, ldr_value,level="Info"):
    point = Point("lamp_status") \
        .tag("lamp_id", lamp_id) \
        .tag("level",str(level))\
        .tag("label",str(label))\
        .field("status", str(status)) \
        .field("confidence", float(confidence)) \
        .field("ldr", int(ldr_value)) \
        .field("reason" , str(reason))\
        .time(datetime.utcnow())
    write_api.write(bucket=bucket, org=org, record=point)