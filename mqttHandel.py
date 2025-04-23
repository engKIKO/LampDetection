import paho.mqtt.client as mqtt


# MQTT Broker configuration
BROKER = 'broker.hivemq.com'  # Or use your own (e.g., Mosquitto or HiveMQ cloud)
PORT = 1883
TOPIC_LDR = 'sensor/ldr'
TOPIC_LOG = 'lamp/logs'



# Low light threshold (e.g., from LDR sensor)
LDR_THRESHOLD = 300  # Adjust based on your LDR scale
is_night = False  # Global state updated from LDR

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_LDR)  # Subscribing to LDR topic

def on_message(client, userdata, msg):
    global is_night
    try:
        ldr_value = int(msg.payload.decode())
        print(f"[LDR] Received value: {ldr_value}")

        # Update time-based condition
        is_night = ldr_value < LDR_THRESHOLD
    except ValueError:
        print("Received invalid LDR value.")

def publish_log(message):
    print(f"[MQTT] Publishing log: {message}")
    client.publish(TOPIC_LOG, message)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start():
    client.connect(BROKER, PORT, 60)
    client.loop_start()

def stop():
    client.loop_stop()
    client.disconnect()