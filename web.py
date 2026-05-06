import cv2 as cv
import mediapipe as mp
import numpy as np
import requests


mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands
video=cv.VideoCapture(0)

ESP32_IP = "192.168.1.33"
ESP32_URL = f"http://{ESP32_IP}/status"

def send_to_esp32(data):
    try:
        requests.post(ESP32_URL, json={"array": data}, timeout=1)
    except Exception as e:
        pass

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while True:
        _,frame=video.read()
        frame=cv.flip(frame,1)
        image=cv.cvtColor(frame,cv.COLOR_BGR2RGB);
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            count=[0]*5
            Position=(50,100)
            for num,hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
                landmarks=hand.landmark
                if landmarks[8].y < landmarks[6].y:
                    count[1]=1
                if landmarks[12].y < landmarks[10].y:
                    count[2]=1
                if landmarks[16].y < landmarks[14].y:
                    count[3]=1
                if landmarks[20].y < landmarks[18].y:
                    count[4]=1
                if landmarks[3].x > landmarks[4].x:
                    count[0]=1
            for i in range(5):
                status = "ON" if count[i] else "OFF"
                cv.putText(image, f"Servo {i+1}:{status}",
                          Position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                Position=tuple(np.array(Position) + np.array((0,40)))
            send_to_esp32(count)





        cv.imshow("Hand tracking",image)
        if cv.waitKey(20) &  0XFF==ord('q'):
            break
video.release()
cv.destroyAllWindows()

