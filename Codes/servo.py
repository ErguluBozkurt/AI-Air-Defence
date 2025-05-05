import RPi.GPIO as GPIO
import time

# Servo motor için pin
SERVO_PIN = 14  # Servo motor sinyal pini

# GPIO ayarları
GPIO.setmode(GPIO.BCM)

# Servo motor için GPIO ayarları
GPIO.setup(SERVO_PIN, GPIO.OUT)
p_servo = GPIO.PWM(SERVO_PIN, 50)  # Servo için 50 Hz PWM frekansı
p_servo.start(0)  # Başlangıçta servo 0 derece

# Servo motoru belirli bir açıya döndüren fonksiyon
def set_angle(angle):
    duty_cycle = (angle / 18) + 2  # Açıyı duty cycle'a çevir (2 ile 12 arası)
    p_servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Servonun hareket etmesi için bekle
    p_servo.ChangeDutyCycle(0)  # Titreşimi önlemek için duty cycle'ı sıfırla

while True:
    # Servo motoru 60 dereceye döndür
    set_angle(0)

    # 60 derece ileri döndür
    set_angle(60)
