# This program allows a user to enter a
# Code. If the C-Button is pressed on the
# keypad, the input is reset. If the user
# hits the A-Button, the input is checked.
import RPi.GPIO as GPIO
from gpiozero import Buzzer
import time

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

secretCode = "4789"
input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global input
    pressed = False

    #GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("Input reset!");
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C4) == 1):
        if input == secretCode:
            print("Code correct!")
            #This part to "return 1" is all testing and may be deleted!!!!!!
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(1, GPIO.OUT)

            servo=GPIO.PWM(1, 50)
            servo.start(0)

            servo.ChangeDutyCycle(10) # left -90 deg position
            time.sleep(5)
            #servo.ChangeDutyCycle(-10) # neutral position

            servo.stop()
            
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
            
            LED_PIN = 27
            
            GPIO.setup(LED_PIN, GPIO.OUT)
            
            buzzer = Buzzer(25)
            
            while True:
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(1)
                buzzer.on()
                time.sleep(1)
                buzzer.off()
                time.sleep(1)
            
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
            
            #This is the end of the testing code!!!!!!!
            #return 1
            # TODO: Activate Sensor/Motor to move Sensor
        else:
            print("Incorrect code!")
            buzzer.on()
            time.sleep(1)
            buzzer.off()
            #return 0
            # TODO: Light up LED and Activate Buzzer
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            if not checkSpecialKeys():
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    print("\nApplication stopped!")
