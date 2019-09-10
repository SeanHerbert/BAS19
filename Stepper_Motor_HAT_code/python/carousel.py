
import RPi.GPIO as GPIO
import time
from DRV8825_scratch import DRV8825

class carousel:
    def __init__(self):
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.steps = 0
        self.curPos = 1
    
    def stepForward(self):
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001)
        self.steps += 32
        self.steps = self.steps%6400
    def stepBackward(self):
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        self.steps -= 32
        self.steps = self.steps%6400
    def nextSlide(self):
        self.motor.TurnStep(Dir='forward', steps=320, stepdelay = 0.000001)
        self.steps += 320
        self.curPos+=1
        self.curPos = self.curPos % 20
        self.steps = self.steps%6400
    def prevSlide(self):
        self.motor.TurnStep(Dir='backward', steps=320, stepdelay = 0.000001)
        self.steps -= 320
        self.curPos-=1
        self.curPos = self.curPos % 20
        self.steps = self.steps%6400
    def zeroPos(self):
        self.curPos = 1
        self.steps = 0
    def moveToSlide(self, next):
        print(self.curPos)
        if(self.curPos<next and (next-self.curPos)<11):
            turns = (next-self.curPos)
            print(turns)
            for x in range(0,turns):
                self.nextSlide()
            self.curPos = next
        elif(self.curPos<next and (next-self.curPos)>=11):
            turns = (self.curPos -next)%20
            print(turns)
            for x in range(0,turns):
                self.prevSlide()
            self.curPos = next
        elif(self.curPos>next and (self.curPos-next)<11):
            turns = (self.curPos -next)
            for x in range(0,turns):
                self.prevSlide()
            self.curPos = next
        elif(self.curPos>next and (self.curPos-next)>=11):
            turns = (next -self.curPos)%20
            for x in range(0,turns):
                self.nextSlide()
            self.curPos = next
            
        
        
    
        
    