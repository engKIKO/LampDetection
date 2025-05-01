import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

# MQTT Broker configuration
BROKER = os.getenv("BROKER")
PORT = os.getenv("BROKER_PORT")
TOPIC_LDR = os.getenv("TOPIC_LDR")
TOPIC_LOG = os.getenv("TOPIC_LOG")



# Low light threshold (e.g., from LDR sensor)
LDR_THRESHOLD = 1000  # Adjust based on your LDR scale

# Internal state
_mqtt_state = {
    'ldr_value': None
}
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_LDR)  # Subscribing to LDR topic

def on_message(client, userdata, msg):
    try:
        value = int(msg.payload.decode())
        print(f"[MQTT] LDR received: {value}")
        _mqtt_state['ldr_value'] = value
    except ValueError:
        print("[MQTT] Invalid LDR value")

def publish_log(message):
    print(f"[MQTT] Publishing log: {message}")
    client.publish(TOPIC_LOG, message)

def LDR_is_night():
    val = _mqtt_state.get('ldr_value')
    if val is None:
        return False  # Default if no value received yet
    return val < LDR_THRESHOLD
  
def get_ldr_value():
    print(_mqtt_state.get('ldr_value'))
    return _mqtt_state.get('ldr_value')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    client.connect(BROKER, PORT, 60)
    client.loop_start()

def stop():
    client.loop_stop()
    client.disconnect()