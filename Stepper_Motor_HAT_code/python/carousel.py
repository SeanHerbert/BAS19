
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

class carousel:
    def __init__(self):
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.steps = 0
    
    def stepForward(self):
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001)
        self.steps += 32
    def stepBackward(self):
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        self.steps -= 32
    def nextSlide(self):
        self.motor.TurnStep(Dir='forward', steps=320, stepdelay = 0.000001)
        self.steps += 320
    def prevSlide(self):
        self.motor.TurnStep(Dir='backward', steps=320, stepdelay = 0.000001)
        self.steps -= 320
    def zerPos(self):
        self.steps = 0
    
        
    