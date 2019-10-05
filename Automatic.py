from carousel import carousel
from Focus import Focus
from BloodCounter import BloodCounter
from FileHandler import FileHandler
from tkinter import BOTH, END, LEFT
import time


class Automatic():
    def __init__(self,system):
        self.system = system
        self.fileHandler = FileHandler(self)
        
    def start(self):
        self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(3,4))
        for i in range(20):
            #auto focus
            bestImage = self.system.focus.autoFocus()
            #analyze image
            x = self.system.bloodCounter.countWBC(bestImage)
            y = self.system.bloodCounter.countRBC(bestImage)
            z = self.system.bloodCounter.calcRatio()
            
            self.fileHandler.writeRatio(i, z)
            self.system.carousel.nextSlide()
#             time.sleep(1)
            self.system.GUI.sampleBloodCountText.delete("1.0", "end")
            self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(x,y))
            self.system.GUI.sampleRatioText.delete("1.0", "end")
            self.system.GUI.sampleRatioText.insert(END,z)
#             time.sleep(1)

    
        
        
        
        
    
    