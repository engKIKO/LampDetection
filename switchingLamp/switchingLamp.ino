#define NUM_LEDS 10
int ledPins[NUM_LEDS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};  // You can change these pins

void setup() {
  Serial.begin(115200);  // Start Serial Monitor
  delay(2000); // wait for serial connection
  Serial.println("ESP32 is alive!");
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  // Initialize all LEDs OFF
  }
  Serial.println("Ready. Type command like 3,1 or 5,0");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');  // Read until newline
    input.trim();  // Remove whitespace

    int commaIndex = input.indexOf(',');
    if (commaIndex > 0 && commaIndex < input.length() - 1) {
      int ledNum = input.substring(0, commaIndex).toInt();
      int state = input.substring(commaIndex + 1).toInt();

      if (ledNum >= 1 && ledNum <= NUM_LEDS && (state == 0 || state == 1)) {
        digitalWrite(ledPins[ledNum - 1], state);
        Serial.print("LED ");
        Serial.print(ledNum);
        Serial.print(state ? " ON" : " OFF");
        Serial.println();
      } else {
        Serial.println("Invalid LED number or state.");
      }
    } else {
      Serial.println("Invalid command. Use format: <led>,<0|1>");
    }
  }
}
