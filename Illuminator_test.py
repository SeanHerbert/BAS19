import RPi.GPIO as io
io.setwarnings(False)

import time
import random
from Illuminator import Illuminator

brightness = 31 # (0-31)
dataPin = 14 ; clockPin = 15 # GPIO pin names
red = 0; green = 255; blue = 0; # values between 0-255
switch = 1

led = Illuminator(dataPin,clockPin,brightness)
led.turnOn()
time.sleep(2)
i=0
while(1):
    green =(green +222) %256
    blue = (blue+100)%256
    red = (red+ 154)%256
    if(i == 4):
        led.turnOff()
    led.changeColor((red,green,blue))
    
#    if(i%2 ==1):
#        led.setBrightness(31)
#    else:
#        led.setBrightness(1)
#    led.on((green,blue,red)) 
    
    time.sleep(2)
#    led.off()
##    led.off()
#    
#    time.sleep(1)
    i+=1
     

