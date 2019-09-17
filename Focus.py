
import cv2
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from imutils import paths

class Focus():
    def __init__(self):
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.curPos = self.goToMax()
        self.maxPos = 35
        self.minPos = 25
    
    def varianceofLap(image):
        return cv2.Laplacian(image,cv2.CV_64F).var()

    def goToMax(self):
        #moveToMax pos
        max = 35
        return max

    def vidOn(self):
        print("vidOn")
        
    
    
    def vidOff(self):
        print("vidOff")
        
    
    def autoFocus(self):
        # for imagePaths in paths.list_images('images'):
        #     image = cv2.imread(imagePaths)
        #     imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        loop = 0
        lt = 0
        i=0

        for imagePaths in paths.list_images('images'):
            image = cv2.imread(imagePaths)
            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            v = self.varianceofLap(imageGray)
            if(i==0):
                lt=v
                i+=1
                self.jogDown()
                continue
            else:
                if(v>lt):
                    lt=v
                    self.jogDown()
                    continue
                else:
                    if(loop>3):
                        break
                    else:
                        loop += 1
                        if(self.curPos<=self.minPos):
                            self.jogUp()
                            lt = v
                            continue
                        else:
                            self.jogDown()
                            lt = v
                            continue









    def zVar(self):
        print("zVar")
        
    
    
    def setStop(self):
        print("setStop")
        
    
    def jogUp(self):
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        
    
    def jogDown(self):
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001)
        
        
        
    
        
    
