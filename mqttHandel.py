import paho.mqtt.client as mqtt


# MQTT Broker configuration
BROKER = 'localhost'  # Or use your own (e.g., Mosquitto or HiveMQ cloud)
PORT = 1883
TOPIC_LDR = 'sensor/ldr'
TOPIC_LOG = 'lamp/logs'



# Low light threshold (e.g., from LDR sensor)
LDR_THRESHOLD = 300  # Adjust based on your LDR scale
LDR_is_night = False  # Global state updated from LDR

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