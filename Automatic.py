from FileHandler import FileHandler
from tkinter import END



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
            self.fileHandler.writeRatio(self.system.control.wb,self.system.control.ws1,i, z)
            self.fileHandler.writeDateTime(self.system.control.wb,self.system.control.ws1,i)
            self.system.GUI.sampleBloodCountText.delete("1.0", "end")
            self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(x,y))
            self.system.GUI.sampleRatioText.delete("1.0", "end")    
            self.system.GUI.sampleRatioText.insert(END,"{}".format(z))
            self.system.GUI.sampleIdText.delete("1.0", "end")
            self.system.carousel.nextSlide()
            print("===============================SLIDE {} COMPLETE========================".format(i))
        return 'done'

    
        
        
        
        
    
    