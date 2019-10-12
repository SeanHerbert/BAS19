from carousel import carousel
from Focus import Focus
from BloodCounter import BloodCounter
from FileHandler import FileHandler
from tkinter import BOTH, END, LEFT
import time
from threading import Thread



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
#             t.start()
            
    #             time.sleep(1)
            self.system.GUI.sampleBloodCountText.delete("1.0", "end")
            
            self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(x,y))
            self.system.GUI.sampleRatioText.delete("1.0", "end")
            if(float(z)>float(self.system.util.maxPathology) or float(z) <float(self.system.util.minPathology)):
                self.sampleRatioText.configure(highlightbackground="red")
                self.sampleRatioText.configure(highlightthickness=4)
            else:
                self.sampleRatioText.configure(highlightthickness=0)
                
            self.system.GUI.sampleRatioText.insert(END,"{}+{}".format(z,self.system.carousel.curPos))
            self.system.GUI.sampleIdText.delete("1.0", "end")
#             self.system.GUI.sampleIdText.insert(END,"{}".format(self.system.carousel.curPos))
            self.system.carousel.nextSlide()
#             time.sleep(1)
        return 'done'

    
        
        
        
        
    
    