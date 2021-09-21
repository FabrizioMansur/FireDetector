import numpy as np
import cv2
from playsound import playsound
import sys
import os
import requests


def sendsms():
    resp = requests.post('https://textbelt.com/text', {
        'phone': '+XXXXXXXXXXXXX',
        'message': "PERICOLO D'INCENDIO! FUOCO RILEVATO IN CASA!!!",
        'key': 'textbelt',
    })
    print(resp.json())


fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 255), 4)
        cv2.putText(frame, "FUOCO!", (x - 20, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        print("fire is detected")
        playsound('audio.mp3')
        sendsms()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
