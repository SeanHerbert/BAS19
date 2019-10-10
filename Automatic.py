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
#         self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(3,4))
        for i in range(20):
            if(self.system.control.stop_threads.is_set()):
                break
                #auto focus
            bestImage = self.system.focus.autoFocus()
                #analyze image
            print("best image found")
            if(self.system.control.stop_threads.is_set()):
                break
            x = self.system.bloodCounter.countWBC(bestImage)
            if(self.system.control.stop_threads.is_set()):
                break
            y = self.system.bloodCounter.countRBC(bestImage)
            if(self.system.control.stop_threads.is_set()):
                break
            z = self.system.bloodCounter.calcRatio()
            if(self.system.control.stop_threads.is_set()):
                break    
            self.fileHandler.writeRatio(i, z)
            
    #             time.sleep(1)
            self.system.GUI.sampleBloodCountText.delete("1.0", "end")
            
            self.system.GUI.sampleBloodCountText.insert(END,"{}/{} +{}".format(x,y,self.system.carousel.curPos))
            self.system.GUI.sampleRatioText.delete("1.0", "end")
            self.system.GUI.sampleRatioText.insert(END,"{}+{}".format(z,self.system.carousel.curPos))
            self.system.GUI.sampleIdText.delete("1.0", "end")
            self.system.GUI.sampleIdText.insert(END,"CS is {}".format(self.system.carousel.curPos))
            self.system.carousel.nextSlide()
#             time.sleep(1)

    
        
        
        
        
    
    