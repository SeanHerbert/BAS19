import RPi.GPIO as GPIO
import time
from DRV8825_scratch import DRV8825
from carousel import carousel


try:
    
#    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
#    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
#    
#   
#    for x in range(0, 200):   
        #Motor1.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)
        #time.sleep(0.5)
        #Motor1.TurnStep(Dir='backward', steps=6400, stepdelay = 0.000001)
        #Motor1.Stop()
    
#       c = carousel()
#       c.prevSlide()
        

        c = carousel()
        c.zeroPos()
        c.moveToSlide(20)
        time.sleep(4)
        c.moveToSlide(6)
        time.sleep(4)
        c.moveToSlide(11)
        time.sleep(4)
        c.moveToSlide(9)
        
        
    
   
    #Motor2.SetMicroStep('hardward' ,'halfstep')    
    #Motor2.TurnStep(Dir='forward', steps=2048, stepdelay=0.002)
    #time.sleep(0.5)
    #Motor2.TurnStep(Dir='backward', steps=2048, stepdelay=0.002)
    #Motor2.Stop()
    
except:
    # GPIO.cleanup()
    print ("\nMotor stop")
    c.motor.Stop()
    #Motor2.Stop()
    exit()