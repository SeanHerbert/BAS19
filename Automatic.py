from FileHandler import FileHandler
from tkinter import END
import time

from threading import Thread



class Automatic():
    def __init__(self,system):
        self.system = system
        self.fileHandler = FileHandler(self)
        
#     def analyze(self):
#         x = self.system.bloodCounter.countWBC(self.bestImage)
#         if(self.system.control.stop_threads.is_set()):
#             return
#         y = self.system.bloodCounter.countRBC(self.bestImage)
#         if(self.system.control.stop_threads.is_set()):
#             return
#         z = self.system.bloodCounter.calcRatio()
#         if(self.system.control.stop_threads.is_set()):
#             return
#         pathFlag = self.system.util.pathologyWarn(z)
# #         dataArray = ['update_auto',x,y,z,pathFlag,i]
# #         self.system.GUI.queue.put(dataArray)
# #             print("Right after: ",self.system.GUI.queue.get(0))
# #             time.sleep(5)
#             
#         self.fileHandler.writeRatio(self.system.control.wb,self.system.control.ws1,self.i, z, pathFlag)
#         self.fileHandler.writeDateTime(self.system.control.wb,self.system.control.ws1,self.i)
#         self.fileHandler.writePathology(self.system.control.wb,self.system.control.ws1,self.i,z)
#         return
        
    def start(self):
#         self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(3,4))
        
            
        for i in range(20):
            
            if(self.system.control.stop_threads.is_set()):
                break
                #auto focus
            self.system.focus.autoFocus()
                #analyze image
            
            bestImage = self.system.currImage_analyze
            
            
            print("best image found")
            
#             th = Thread(target = self.analyze)
#             th.start()
            
            
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
            pathFlag = self.system.util.pathologyWarn(z)
            dataArray = ['update_auto',x,y,z,pathFlag,i]
            self.system.GUI.queue.put(dataArray)
#             print("Right after: ",self.system.GUI.queue.get(0))
#             time.sleep(5)
            
            self.fileHandler.writeRatio(self.system.control.wb,self.system.control.ws1,i, z, pathFlag)
            self.fileHandler.writeDateTime(self.system.control.wb,self.system.control.ws1,i)
            self.fileHandler.writePathology(self.system.control.wb,self.system.control.ws1,i,z)
            
            
            
            
#             print("contents of queue before data Insert",self.system.GUI.queue.get(0))
            
#             print("Array data put into the queue :",self.system.GUI.queue.get(0))
#             self.system.GUI.sampleBloodCountText.delete("1.0", "end")
#             self.system.GUI.sampleBloodCountText.insert(END,"{}/{}".format(x,y))
#             self.system.GUI.sampleRatioText.delete("1.0", "end")    
#             self.system.GUI.sampleRatioText.insert(END,"{}".format(z))
#             self.system.GUI.sampleIdText.delete("1.0", "end")
#             self.system.GUI.goToSlideText.delete("1.0","end")
#             self.system.GUI.goToSlideText.insert(END,i)
            
            self.system.carousel.nextSlide()
            print("moved carousel")
            print("===============================SLIDE {} COMPLETE========================".format(i))
        return 'done'

    
        
        
        
        
    
    

