import cv2
import numpy as np
from collections import deque
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

buffer_size = 16 # deque nun boyutu 
pts = deque(maxlen=buffer_size)

blue_lower = (100, 150, 0) # (H,S,V) Rengimiz mavi.
blue_upper = (150, 255, 255)

# Kamerayı aç
picam2 = Picamera2()
picam2.preview_configuration.main.size = (720, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# GPIO pinlerini tanımla
gpio_x = [17,27,22,10] # A, B, C, D # ör. GPIO 17
gpio_y = [14,15,18,23] 

# GPIO modunu belirle
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_x, GPIO.OUT)
GPIO.setup(gpio_y, GPIO.OUT)

# Half-step sürüş dizisi
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
    """Step motoru belirtilen adım sayısı kadar döndürür."""
    for _ in range(steps):
        for step in step_sequence[::direction]:  # İleri veya geri yönde git
            GPIO.output(gpio, step)
            time.sleep(delay)


            
# Setup for servo motor
servo_pin = 2  # Pin for servo motor
# Setup PWM for the servo
servo = GPIO.PWM(servo_pin, 50)  # 50Hz frequency for the servo
servo.start(0)  # Initial position

# Function to move servo to 90 degrees and back to 0
def move_servo():
    # Move to 90 degrees
    servo.ChangeDutyCycle(12.5)  # Position for 90 degrees
    time.sleep(0.3)  # Wait for the servo to move
    # Move back to 0 degrees
    servo.ChangeDutyCycle(2.5)  # Position for 0 degrees
    time.sleep(0.3)  # Wait for the servo to move
    servo.ChangeDutyCycle(0)  # Stop sending signal to the servo


while True:
    frame = picam2.capture_array()
    
    # blur
    blured = cv2.GaussianBlur(frame, (11,11), sigmaX=7)
    # HSV
    hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV Image", hsv)

    # mavi için maske oluştur
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    cv2.imshow("Mask Image", mask)

    # Gürültü var azaltmak için erozyon ve genişleme kullan
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    cv2.imshow("Mask + Erozyon + Genişleme Image", mask)

    # Kontur
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if(len(contours) > 0):
        c = max(contours, key=cv2.contourArea) 
        rect = cv2.minAreaRect(c) # diktörtgen ile çevir
        ((x,y), (width, height), rotation) = rect

        box = cv2.boxPoints(rect) # kutucuk yapalım
        box = np.int64(box)
        
        mom = cv2.moments(c) # görüntünün merkezini bulur
        center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))

        diff_x = 360 - center[0] # ekranın ortası - tespit edilen nesnenin orta noktası.  -300 ile +300
        diff_y = 240 - center[1] # -180 ile +180

        s = f"x : {np.round(x)} y : {np.round(y)} width : {np.round(width)} height : {np.round(height)} rotation : {np.round(rotation)}"
        s1 = f"X-axis stepper motor :{diff_x} Y-axis stepper motor : {diff_y}"
        cv2.drawContours(frame, [box], 0,( 0,255,255), 2)# kontoru çizdir. renk : sarı, kalınlık : 2
        cv2.circle(frame, center, 5, (255,0,255), -1) # merkeze bir nokta koyalım. center : merkeze, 5 : yarıçap, renk : pembe, -1 : doldur içini
        cv2.putText(frame, s, (20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1) # 20,30 kordinatları, renk: siyah, kalınlık: 1
        cv2.putText(frame, s, (20,70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 1) # 20,30 kordinatları, renk: siyah, kalınlık: 1

         # Adjust X-axis stepper motor
        if diff_x > 0:  # If the object is not centered horizontally
            STEP_COUNT_X = 2048 / 300-abs(center[0])
            step_motor(STEP_COUNT_X, gpio_x, direction=1) # Saat yönünde döndür. Move right
            if diff_y > 0:
                STEP_COUNT_Y = 2048 / 180-abs(center[1])
                step_motor(STEP_COUNT_Y, gpio_y, direction=-1)  # Saat yönünün tersine geri döndür. Move down
                
            elif diff_y < 0:
                STEP_COUNT_Y = 2048 / 180-abs(center[1])
                step_motor(STEP_COUNT_Y, gpio_y, direction=1)  # Saat yönünde döndür. Move up

        
        elif diff_x < 0:  # If the object is not centered vertically
            STEP_COUNT_X = 2048 / 300-abs(center[0])
            step_motor(STEP_COUNT_X, gpio_x, direction=-1) 
            if diff_y > 0: 
                STEP_COUNT_Y = 2048 / 180-abs(center[1])
                step_motor(STEP_COUNT_Y, gpio_y, direction=-1) 
            elif diff_y < 0:
                STEP_COUNT_Y = 2048 / 180-abs(center[1])
                step_motor(STEP_COUNT_Y, gpio_y, direction=1)


        if(abs(abs(diff_x) - center[0]) <= 10 and abs(abs(diff_y) - center[0]) <= 10):
            move_servo()
        if(abs(abs(diff_x) - center[0]) >= 10 or abs(abs(diff_y) - center[0]) >= 10):
            servo.stop()


    # çizgi ile takip algoritması
    pts.appendleft(center)
    for i in range(1, len(pts)): # çizginin uzunluğu tanımlanan deque ile değişmektedir.
        if(pts[i-1] is None or pts[i] is None):
            continue
        cv2.line(frame, pts[i-1], pts[i], (0,255,0), 3) # yeşil çizgi, kalınlık : 3

    cv2.imshow("Image", frame)

    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break



# Clean up
GPIO.cleanup()
cv2.destroyAllWindows()
