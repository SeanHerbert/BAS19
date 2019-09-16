
import cv2
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from imutils import paths

class Focus():
    def __init__(self):
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        
    
    def varianceofLap(image):
        return cv2.Laplacian(image,cv2.CV_64F).var()

    def vidOn(self):
        print("vidOn")
        
    
    
    def vidOff(self):
        print("vidOff")
        
    
    def autoFocus(self):
        print("autoFocus")
    
    
    def zVar(self):
        print("zVar")
        
    
    
    def setStop(self):
        print("setStop")
        
    
    def jogUp(self):
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        
    
    def jogDown(self):
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001)
        
        
        
    
        
    