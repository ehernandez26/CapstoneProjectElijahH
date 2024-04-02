#prepares code to use the LED and sleep functions
from gpiozero import LED
from time import sleep

#sets x (amount of loops) to 0
x = 0

#while loop that turns an LED on using the pin according to an input from the user
while x <= 5:
  red = LED(input("Pin: "))

#the LED turns on for 2 seconds then turns off
  red.on()
  sleep(2)
  red.off()

#adds 1 to the amount of loops, so that the while loop will eventually stop
  x = x + 1
