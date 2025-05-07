# DC motor ve servo ekli değil. Şuan sadece nesneyi tespit etmesini ve step motorlar ile onu takip etmesi gerekiyor

import cv2
import numpy as np
from collections import deque
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time
from ultralytics import YOLO

buffer_size = 16
pts = deque(maxlen=buffer_size)

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLO model trained to detect blue objects
model = YOLO("best.pt")

# GPIO pin setup
gpio_x = [5, 6, 13, 26]
gpio_y = [1, 7, 8, 12]
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_x, GPIO.OUT)
GPIO.setup(gpio_y, GPIO.OUT)

# Half-step sequence
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def step_motor(steps, gpio, direction, delay=0.002):
    for _ in range(int(steps)):
        for step in step_sequence[::direction]:
            GPIO.output(gpio, step)
            time.sleep(delay)


while True:
    frame = picam2.capture_array()

    results = model(frame)[0]
    center = None

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        x1, y1, x2, y2, class_id = int(x1), int(y1), int(x2), int(y2), int(class_id)

        if score > 0.2:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            class_name = results.names[class_id]
            score_percent = round(score * 100, 2)
            text = f"{class_name}:{score_percent}%"
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 255, 255), 1)

            obj_center_x = (x1 + x2) // 2
            obj_center_y = (y1 + y2) // 2
            center = (obj_center_x, obj_center_y)

            diff_x = 360 - obj_center_x
            diff_y = 240 - obj_center_y

            s = f"x : {obj_center_x} y : {obj_center_y}"
            s1 = f"X-axis stepper motor : {diff_x} Y-axis stepper motor : {diff_y}"
            cv2.circle(frame, center, 5, (255, 0, 255), -1)
            cv2.putText(frame, s, (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 1)
            cv2.putText(frame, s1, (20, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 1)

            if diff_x > 0:
                STEP_COUNT_X = 2048 / (300 - abs(center[0]))
                step_motor(STEP_COUNT_X, gpio_x, direction=1)
                if diff_y > 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    step_motor(STEP_COUNT_Y, gpio_y, direction=-1)
                elif diff_y < 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    step_motor(STEP_COUNT_Y, gpio_y, direction=1)

            elif diff_x < 0:
                STEP_COUNT_X = 2048 / (300 - abs(center[0]))
                step_motor(STEP_COUNT_X, gpio_x, direction=-1)
                if diff_y > 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    step_motor(STEP_COUNT_Y, gpio_y, direction=-1)
                elif diff_y < 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    step_motor(STEP_COUNT_Y, gpio_y, direction=1)

    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), 3)

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Clean up
GPIO.cleanup()
cv2.destroyAllWindows()
