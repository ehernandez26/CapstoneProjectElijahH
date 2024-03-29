from gpiozero import LED
from time import sleep

x = 0

while x <= 5:
  red = LED(input("Pin: "))

  red.on()
  sleep(2)
  red.off()

  x = x + 1
