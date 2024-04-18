import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(1, GPIO.OUT)

servo=GPIO.PWM(1, 50)
servo.start(0)

servo.ChangeDutyCycle(10) # left -90 deg position
sleep(5)
servo.ChangeDutyCycle(-10) # neutral position

servo.stop()
GPIO.cleanup()
