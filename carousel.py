from DRV8825 import DRV8825

#This class controls the carousel motor
#steps variable was never used and modulus might be wrong(but again it was never used so its ok)

class carousel():
    
    #constructor gets system object and creeates motor object 
    def __init__(self,system):
        self.system = system
        self.motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
#         self.motor = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        self.steps = 0
        self.curPos = 0
    
    
    def stepForward(self):
        self.motor.TurnStep(Dir='forward', steps=32, stepdelay = 0.000001) #singe motor step 
        self.steps += 32
        self.steps = self.steps% 38400
        
    def stepBackward(self):
        self.motor.TurnStep(Dir='backward', steps=32, stepdelay = 0.000001)#single motor step 
        self.steps -= 32
        self.steps = self.steps%38400
    
    #moves 60 motor steps due to gear ratio 
    def nextSlide(self):
        if (not self.system.control.stop_threads.is_set()):
            self.motor.TurnStep(Dir='forward', steps=1920, stepdelay = 0.000001)
            self.steps += 1920
            self.curPos+=1
            self.curPos = (self.curPos % 20)
            self.steps = self.steps%38400
    
    #moves 60 motor steps due to gear ratio
    def prevSlide(self):
        self.motor.TurnStep(Dir='backward', steps=1920, stepdelay = 0.000001)
        self.steps -= 1920
        self.curPos-=1
        self.curPos = (self.curPos % 20) 
        self.steps = self.steps%38400
    
    #sets curPos to zero
    def zeroPos(self):
        self.curPos = 0
        self.steps = 0
    
    #moves to slide input by user through the shortest path 
    def moveToSlide(self, next):
        if(self.curPos<next and (next-self.curPos)<11):
            turns = (next-self.curPos)
            for x in range(0,turns):
                self.nextSlide()
            self.curPos = next
        elif(self.curPos<next and (next-self.curPos)>=11):
            turns = (self.curPos -next)%20
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
            
        
        
    
        
    