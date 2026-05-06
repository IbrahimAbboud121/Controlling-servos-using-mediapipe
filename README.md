Hand-Controlled Servo System
A real-time hand tracking system that controls 5 servos using finger gestures. The ESP32 receives commands via WiFi and controls servos based on which fingers are raised.
demo:https://youtu.be/QQHYMY6QE4A?si=PX8noRMQ8AScppSa
Hardware Requirements
ESP32 development board

5 Servo motors (e.g., SG90, MG995)

USB Camera (for PC/laptop)

Wiring
Servo	ESP32 Pin
Servo 0	GPIO 16
Servo 1	GPIO 17
Servo 2	GPIO 18
Servo 3	GPIO 19
Servo 4	GPIO 21
Connect all servo grounds to ESP32 GND and power appropriately (external power recommended for multiple servos)

Software Setup
1. ESP32 (Arduino IDE)
Requirements:

Install ESP32 board package

Install libraries: WiFi, WebServer, ESP32Servo

Configuration:

cpp
const char* ssid = "TP-Link_0680";  // Your WiFi name
const char* pass = "73334712";       // Your WiFi password
Upload the ESP32 code and note the IP address from Serial Monitor.

2. Python Client (PC)
Install dependencies:

bash
pip install opencv-python mediapipe requests numpy
Configuration:

python
ESP32_IP = "192.168.1.33"  # Change to your ESP32's IP
How It Works
Finger	Servo	Gesture
Thumb	Servo 1	Thumb extended away from index
Index	Servo 2	Index finger raised
Middle	Servo 3	Middle finger raised
Ring	Servo 4	Ring finger raised
Pinky	Servo 5	Pinky finger raised
Finger UP → Servo rotates (0°)

Finger DOWN → Servo stops (90°)

Usage
Upload code to ESP32

Run Python script: python hand_control.py

Show your hand to the camera

Raise/lower fingers to control servos

Press q to exit the Python program.

Troubleshooting
ESP32 not connecting to WiFi → Check SSID/password

No servo movement → Verify power supply and pin connections

Python can't reach ESP32 → Ensure both devices on same network; check IP address

Slow response → Reduce distance between devices or improve WiFi signal
