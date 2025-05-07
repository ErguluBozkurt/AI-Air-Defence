# dcmotor.py
import RPi.GPIO as GPIO

# Motor pin tanımlamaları
ENA = 22
INA = 27
INB = 17

ENB = 25
INC = 23
IND = 24

# PWM nesneleri global
p_m1 = None
p_m2 = None

def setup_motors():
    global p_m1, p_m2

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)

    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(INC, GPIO.OUT)
    GPIO.setup(IND, GPIO.OUT)

    GPIO.output(INA, GPIO.LOW)
    GPIO.output(INB, GPIO.LOW)
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.LOW)

    p_m1 = GPIO.PWM(ENA, 1000)
    p_m1.start(0)

    p_m2 = GPIO.PWM(ENB, 1000)
    p_m2.start(0)

def start_motors(speed=10):
    # Motor 1 ileri
    GPIO.output(INA, GPIO.HIGH)
    GPIO.output(INB, GPIO.LOW)
    p_m1.ChangeDutyCycle(speed)

    # Motor 2 geri
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.HIGH)
    p_m2.ChangeDutyCycle(speed)

def stop_motors():
    GPIO.output(INA, GPIO.LOW)
    GPIO.output(INB, GPIO.LOW)
    GPIO.output(INC, GPIO.LOW)
    GPIO.output(IND, GPIO.LOW)
    p_m1.ChangeDutyCycle(0)
    p_m2.ChangeDutyCycle(0)

def cleanup():
    GPIO.cleanup()
