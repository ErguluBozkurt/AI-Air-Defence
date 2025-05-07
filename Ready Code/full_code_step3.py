# full_code_step2.py gibi tüm sistem çalışıyor fakat servo, step ve dc motorların her biri farklı bir scripte yazıldı.

import cv2
import numpy as np
from collections import deque
from picamera2 import Picamera2
from ultralytics import YOLO
import dcmotor  
import servomotor  
import stepmotor  

buffer_size = 16
pts = deque(maxlen=buffer_size)

# Kamera başlatma
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# YOLO modelini yükleme
model = YOLO("best.pt")

# Motorları başlat
dcmotor.setup_motors()

# Çerçeve üzerinde obje takip işlemi
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

            # Step motor hareketleri
            if diff_x > 0:
                STEP_COUNT_X = 2048 / (300 - abs(center[0]))
                stepmotor.step_motor(STEP_COUNT_X, stepmotor.gpio_x, direction=1)
                if diff_y > 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    stepmotor.step_motor(STEP_COUNT_Y, stepmotor.gpio_y, direction=-1)
                elif diff_y < 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    stepmotor.step_motor(STEP_COUNT_Y, stepmotor.gpio_y, direction=1)

            elif diff_x < 0:
                STEP_COUNT_X = 2048 / (300 - abs(center[0]))
                stepmotor.step_motor(STEP_COUNT_X, stepmotor.gpio_x, direction=-1)
                if diff_y > 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    stepmotor.step_motor(STEP_COUNT_Y, stepmotor.gpio_y, direction=-1)
                elif diff_y < 0:
                    STEP_COUNT_Y = 2048 / (180 - abs(center[1]))
                    stepmotor.step_motor(STEP_COUNT_Y, stepmotor.gpio_y, direction=1)

            # Servo motoru hareket ettir
            if abs(abs(diff_x) - center[0]) <= 10 and abs(abs(diff_y) - center[0]) <= 10:
                dcmotor.start_motors(speed=30)
                servomotor.move_servo()
                dcmotor.stop_motors()

        else:
            servomotor.cleanup()  # Servo motor temizleme
            dcmotor.stop_motors()

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Temizlik işlemleri
dcmotor.cleanup()
servomotor.cleanup()
stepmotor.cleanup()
cv2.destroyAllWindows()
