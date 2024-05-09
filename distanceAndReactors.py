#sets up the codes GPIO, time, and mode
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set pins for the sensor input and output
TRIG = 23
ECHO = 24

#prints a message and sets the input and output of TRIG and ECHO
print('Measuring First Distance')
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

#pauses the sensor for a moment
print('Waiting for First Distance Set')
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

#while loop for setting the time of exit
while GPIO.input(ECHO)==0:
  pulse_firstStart = time.time()

#loop for setting the time of return
while GPIO.input(ECHO)==1:
  pulse_firstEnd = time.time()

#calculates the distance using time of pulse
pulse_firstDuration = pulse_firstEnd - pulse_firstStart
firstDistance = pulse_firstDuration * 17150
firstDistance = round(firstDistance, -1)

print(firstDistance)

#prints a message and sets the input and output of TRIG and ECHO
print('Distance Measurement In Progress')
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

#pauses the sensor for a moment
print('Waiting for Sensor to Settle')
time.sleep(2)

distance = firstDistance

#while loop to continuosly measure distance starts
while distance == firstDistance:
#sets out a burst of waves to measure
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

#while loop for setting the time of exit
  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

#loop for setting the time of return
  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

#calculates the distance using time of pulse
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, -1)
#prints the distance in cm
print('Distance:',distance,'cm')

#Now activate Buzzer and LED
from gpiozero import Buzzer
from time import sleep
import RPi.GPIO as GPIO

LED_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

buzzer = Buzzer(25)

while True:
    GPIO.output(LED_PIN, GPIO.HIGH)
    sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)
    sleep(1)
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)

while True:
    buzzer.beep()


#try:
 #   while True:
  #      GPIO.output(LED_PIN, GPIO.HIGH)
   #     sleep(1)
    #    GPIO.output(LED_PIN, GPIO.LOW)
     #   sleep(1)
#except KeyboardInterrupt:
 #   GPIO.cleanup()
