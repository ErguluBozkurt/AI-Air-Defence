import RPi.GPIO as GPIO
import time

# GPIO setup
SERVO_PIN = 16  # Servo motorun bağlandığı pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Servo motoru çalıştırmak için PWM ayarı
p_servo = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz
p_servo.start(0)

def set_angle(angle):
    duty_cycle = (angle / 18) + 2  # Açıyı duty cycle'a dönüştür
    p_servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Hareketin tamamlanması için süre
    p_servo.ChangeDutyCycle(0)  # Jitteri engelle

def move_servo():
    set_angle(0)
    set_angle(60)

def cleanup():
    p_servo.stop()
    GPIO.cleanup()
