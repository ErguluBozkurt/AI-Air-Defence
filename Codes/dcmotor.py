# L298N Motor Sürücüsü ile 2 DC Motor Kontrolü ve Servo Motor Kontrolü
import RPi.GPIO as GPIO
import servo

# Motor 1 için pinler (İleri yönde dönecek)
ENA = 22  # Motor 1 Enable
INA = 27  # Motor 1 IN1
INB = 17 # Motor 1 IN2

# Motor 2 için pinler (Geri yönde dönecek)
ENB = 25  # Motor 2 Enable
INC = 23  # Motor 2 IN1
IND = 24  # Motor 2 IN2

# GPIO ayarları
GPIO.setmode(GPIO.BCM)

# Motor 1 için GPIO ayarları
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(INA, GPIO.OUT)
GPIO.setup(INB, GPIO.OUT)
GPIO.output(INA, GPIO.LOW)
GPIO.output(INB, GPIO.LOW)
p_m1 = GPIO.PWM(ENA, 1000)  # PWM frekansı 1000 Hz
p_m1.start(0)  # Başlangıçta hız %0


# Motor 2 için GPIO ayarları
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(INC, GPIO.OUT)
GPIO.setup(IND, GPIO.OUT)
GPIO.output(INC, GPIO.LOW)
GPIO.output(IND, GPIO.LOW)
p_m2 = GPIO.PWM(ENB, 1000)  # PWM frekansı 1000 Hz
p_m2.start(0)  # Başlangıçta hız %0

print("\n")
print("Motor kontrol programı başlatıldı.")
print("s - Motorları çalıştır (Motor 1: İleri, Motor 2: Geri) ve Servoyu 60 dereceye döndür")
print("q - Motorları durdur ve Servoyu 0 dereceye döndür")
print("\n")

servo()

while True:
    x = input("Komut girin (start/exit): ")
    if x == 'start':
        print("Motorlar çalıştırılıyor ve Servo 60 dereceye döndürülüyor...")
        # Motor 1: İleri yönde
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        p_m1.ChangeDutyCycle(10)  # %50 hızda çalıştır
        # Motor 2: Geri yönde
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.HIGH)
        p_m2.ChangeDutyCycle(10)  # %50 hızda çalıştır

        print("Motor 1: İleri, Motor 2: Geri, Servo: 60 derece")

    elif x == 'exit':
        print("Motorlar durduruluyor ve Servo 0 dereceye döndürülüyor...")
        # Her iki motoru durdur
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)
        GPIO.output(INC, GPIO.LOW)
        GPIO.output(IND, GPIO.LOW)
        p_m1.ChangeDutyCycle(0)  # Hızı %0 yap
        p_m2.ChangeDutyCycle(0)  # Hızı %0 yap

        # Servo motoru 0 dereceye döndür
        set_servo_angle(0)

        print("Motorlar durduruldu ve Servo 0 dereceye döndürüldü.")
        break
    else:
        print("Geçersiz komut! Lütfen 's' veya 'q' girin.")

# Program sonlandığında GPIO temizleme
GPIO.cleanup()