import RPi.GPIO as GPIO
import math


class Servo:
    def __init__(self, pin, offset=0, limit_left=-math.pi / 2, limit_right=math.pi / 2):
        self.pin = pin
        self.offset = offset
        self.limit_left = limit_left
        self.limit_right = limit_right

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz
        self.pwm.start(2.5 + 5 / math.pi * self.offset)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pwm.stop()

    def set(self, radian):
        actual = radian + self.offset
        if actual > self.limit_right:
            actual = self.limit_right
        elif actual < self.limit_left:
            actual = self.limit_left
        self.pwm.ChangeDutyCycle(2.5 + 5 / math.pi * actual)
