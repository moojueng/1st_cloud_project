import cv2
import os

rtsp_path = 'http://192.168.1.202:50036/?action=stream'

cap = cv2.VideoCapture(rtsp_path)

while True:
    ret, frame = cap.read()
    cv2.imshow("fire_detect_video", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

frame.release()
cv2.destroyallWindow()

