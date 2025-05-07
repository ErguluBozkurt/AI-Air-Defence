import RPi.GPIO as GPIO
import time

# GPIO setup
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

def cleanup():
    GPIO.cleanup()
