import RPi.GPIO as io
io.setwarnings(False)

import time
from Illuminator import Illuminator

brightness=31  
dataPin =14
clockPin=15

led = Illuminator(dataPin,clockPin,brightness)

time.sleep(17)

led.turnOn()

red=0
green=0
blue=0
i=0

time.sleep(18)

led.changeColor(255,0,0)
time.sleep(1.6)
led.changeColor(0,255,0)
time.sleep(1.6)
led.changeColor(0,0,255)
time.sleep(1.6)
led.changeColor(255,255,0)
time.sleep(1.6)
led.changeColor(255,0,255)
time.sleep(1.6)
led.changeColor(0,255,255)
time.sleep(1.6)
led.changeColor(255,0,0)
time.sleep(1.6)
    
    
        
    
led.turnOff()
time.sleep(8)
led.turnOn()
time.sleep(6)
led.turnOff()

     

