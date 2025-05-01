#include <WiFi.h>
#include <PubSubClient.h>

// Wi-Fi config
const char* ssid = "OPPO Reno6 Z 5G";
const char* password = "earn71246";

// MQTT config
const char* mqtt_broker = "broker.emqx.io";
const int mqtt_port = 1883;
const char* pub_topic = "LDR/group5/test"; 

// LDR pin
const int LDR_PIN = 34;

WiFiClient espClient;
PubSubClient client(espClient);

// เชื่อมต่อ WiFi
void setup_wifi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX); 
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_broker, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int lightValue = analogRead(LDR_PIN);
  Serial.print("ค่าความสว่าง: ");
  Serial.println(lightValue);

  char msg[10];
  sprintf(msg, "%d", lightValue);
  client.publish(pub_topic, msg);

  delay(5000); 
}