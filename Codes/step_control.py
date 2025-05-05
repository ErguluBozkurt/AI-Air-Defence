import RPi.GPIO as GPIO
import time
import dcmotor

# Setup for stepper motors
# GPIO pinlerini tanımla
A = 17
B = 27
C = 22
D = 18

# GPIO modunu belirle
GPIO.setmode(GPIO.BCM)
GPIO.setup([A, B, C, D], GPIO.OUT)

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

# 90 derece dönmesi için gereken adım sayısı (Varsayılan: 2048 adım tam tur için)
STEP_COUNT_X = int(2048 / 4)  # 516 = 90 derece için çeyrek tur.
STEP_COUNT_Y = int(2048 / 4)

def step_motor(steps, direction=1, delay=0.002):
    """Step motoru belirtilen adım sayısı kadar döndürür."""
    for _ in range(steps):
        for step in step_sequence[::direction]:  # İleri veya geri yönde git
            GPIO.output([A, B, C, D], step)
            time.sleep(delay)

try:
    print("Step motor 90 derece sağa dönüyor...")
    step_motor(STEP_COUNT_X, direction=1)  # Saat yönünde 90 derece döndür
    
    time.sleep(3) 
    dcmotor()
    print("Step motor eski konumuna dönüyor...")
    step_motor(STEP_COUNT_Y, direction=-1)  # Saat yönünün tersine geri döndür
    time.sleep(3) 
finally:
    GPIO.cleanup()  # GPIO pinlerini temizle
