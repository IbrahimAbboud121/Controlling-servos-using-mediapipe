#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* ssid = "TP-Link_0680";
const char* pass = "73334712";

WebServer server(80);
int receivedData[5] = {0, 0, 0, 0, 0};
int ServosPins[5] = {16, 17, 18, 19, 21};
Servo servos[5];

void setup() {
  for(int i = 0; i < 5; i++) {
    servos[i].attach(ServosPins[i]);
    servos[i].write(90);  // Start stopped
    Serial.print("Servo ");
    Serial.print(i);
    Serial.print(" on pin ");
    Serial.println(ServosPins[i]);
  }

  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println(WiFi.localIP());
  
  server.on("/status", HTTP_POST, []() {
    String json = server.arg("plain");
    
    // Parse digits from JSON
    int idx = 0;
    for(int i = 0; i < json.length() && idx < 5; i++) {
      if(isdigit(json[i])) {
        receivedData[idx] = json[i] - '0';
        idx++;
      }
    }
    
    Serial.print("Received: ");
    for(int i = 0; i < 5; i++) {
      Serial.print(receivedData[i]);
      Serial.print(" ");
    }
    Serial.println();
    
    // Control servos immediately when data is received
    for(int i = 0; i < 5; i++) {
      if(receivedData[i] == 1) {
        servos[i].write(0);   // Rotate
        Serial.print("Servo ");
        Serial.print(i);
        Serial.println(" -> ROTATING");
      } else {
        servos[i].write(90);  // Stop
        Serial.print("Servo ");
        Serial.print(i);
        Serial.println(" -> STOP");
      }
    }
    
    server.send(200, "text/plain", "OK");
  });
  
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}