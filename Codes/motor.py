# L298N Motor Sürücüsü ile 2 DC Motor Kontrolü ve Servo Motor Kontrolü
import RPi.GPIO as GPIO

# Motor 1 için pinler (İleri yönde dönecek)
ENA = 27  # Motor 1 Enable
INA = 17  # Motor 1 IN1
INB = 22 # Motor 1 IN2



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


print("\n")
print("Motor kontrol programı başlatıldı.")
print("s - Motorları çalıştır (Motor 1: İleri, Motor 2: Geri) ve Servoyu 60 dereceye döndür")
print("q - Motorları durdur ve Servoyu 0 dereceye döndür")
print("\n")


while True:
    x = input("Komut girin (start/exit): ")
    if x == 'start':
        print("Motorlar çalıştırılıyor ve Servo 60 dereceye döndürülüyor...")
        # Motor 1: İleri yönde
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        p_m1.ChangeDutyCycle(10)  # %50 hızda çalıştır
     
        print("Motor 1: İleri")

    elif x == 'exit':
        print("Motorlar durduruluyor ve Servo 0 dereceye döndürülüyor...")
        # Her iki motoru durdur
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)
        p_m1.ChangeDutyCycle(0)  # Hızı %0 yap

        print("Motorlar durduruldu ve Servo 0 dereceye döndürüldü.")
        break
    else:
        print("Geçersiz komut! Lütfen 's' veya 'q' girin.")

# Program sonlandığında GPIO temizleme
GPIO.cleanup()