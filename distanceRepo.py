#sets up the codes GPIO, time, and mode
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set pins for the sensor input and output
TRIG = 23
ECHO = 24

#prints a message and sets the input and output of TRIG and ECHO
print('Distance Measurement In Progress')
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

#pauses the sensor for a moment
print('Waiting for Sensor to Settle')
time.sleep(2)

#sets the distance that will be used in the while loop
distance = 0

#while loop to continuosly measure distance starts
while distance <= 1000:
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
  distance = round(distance, 2)
#prints the distance in cm
  print('Distance:',distance,'cm')

#else loop for when the distance >= 10000 which prints a message, and will later activate other code
else:
  print('UH OH!')
