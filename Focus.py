
import cv2
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from imutils import paths
from PIL import Image
from os import walk


class Focus():
    def __init__(self):
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.curPos = self.goToMax()
    
    def varianceofLap(self,image):
        return cv2.Laplacian(image,cv2.CV_64F).var()

    def goToMax(self):
        #moveToMax pos
        #for testing without limit switches, we assuming it takes 5 steps 
        #the for loop will be replaced with the following while loop
        #while(!self.isAtTop()):
        for i in range(5):
            self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001) #probably need to take bigger steps
        print("=====================set to Top===========================")
        return 10000  #10mm from bottom limit switch

    def isAtTop(self):
        #poll top limit switch
        return tls
    
    def isAtBottom(self):
        #poll bottom limit switch
        return bls
    
    def autoFocus(self):
        loop = 0
        lt = 0
        p=0 # used for indexing thru roche images (for testing only)
    
        while(1):
            p+=1 # index thru folders of Roche images
            for (dirpath, dirnames, ifn) in walk('/home/pi/BAS/Images/i'+str(p)):
                f=ifn
            image = cv2.imread('/home/pi/BAS/Images/i'+str(p)+'/'+str(f[0])) #for test: image grabbed from roche images(will be from camera)
            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            v = self.varianceofLap(imageGray)
            print("Variance at folder {} is {}".format(p,v))
            if(loop ==3):
                #For now, just return image from folder (will be from camera)
                return image
                break
            
            if(v>lt):
                lt =v
                self.jogDown()
                
            else:
                lt =v
                self.jogUp()
                p-=2 # used to simulate grabbing the previous image (one jog up)
                loop +=1
                
                    
                



    def zVar(self):
        return self.curPos
        
    def jogUp(self):
        #if(!selfisAtTop()):   //this will poll limit switch
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        self.curPos +=0.5

    def jogDown(self):
        #if(!isAtBottom()):   //this will poll limit switch
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001)
        self.curPos -=0.5
    
    def vidOn(self):
        print("vidOn")
        
    def vidOff(self):
        print("vidOff")
        
        
        
    
        
    
