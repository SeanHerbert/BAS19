from threading import Thread,Event
from openpyxl import load_workbook
import cv2
import numpy as np 

class Controller(object):
    def __init__(self,system):
        self.thread1 = None
        self.thread2 = None
        self.stop_threads = Event()
        self.system = system
#         self.cnt = 0
        

    def loop1(self):
        
        while not self.stop_threads.is_set():
            x = self.system.auto.start()
            if x=='done':
                self.system.GUI.queue.put("setReady")
                self.stop_threads.clear()
                return
        
            
    def loop2(self):
        
#         while not self.stop_threads.is_set():
        self.system.videoThreadStarted = True
        while True:
            
            self.system.cam.startVideo()
            
        self.stop_threads.clear()
        
    def loop3(self):
        while not self.stop_threads.is_set():
            x=self.system.focus.autoFocus()
            if(isinstance(x, (np.ndarray))):
                self.system.GUI.queue.put("setReady")
                
                
                self.stop_threads.clear()
                return
            
        
        


    def combine(self,calledFrom):
        self.calledFrom =calledFrom
        if(self.calledFrom == 'auto'):
            self.system.GUI.updateStatusText("Automatic")
            self.system.GUI.updateStatusBorder("yellow")
            self.system.busy = True
            if(len(self.system.dataFilePaths)==0):
                self.system.util.createFile()
            self.wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
            self.ws1 = self.wb.active
            self.stop_threads.clear()
            self.thread1 = Thread(target = self.loop1)
    #         self.thread2 = Thread(target = self.loop2)
            self.thread1.start()
        if(self.calledFrom =='cam'):
#         self.thread2.start()
          self.stop_threads.clear()
          if(self.system.videoThreadStarted == False):
              self.thread2 = Thread(target = self.loop2)
              self.thread2.start()
              
        if(self.calledFrom == 'focus'):
            
            self.system.GUI.updateStatusText("Autofocusing")
            self.system.GUI.updateStatusBorder("yellow")
            self.system.busy = True
            self.stop_threads.clear()
            self.thread3 = Thread(target=self.loop3)
            self.thread3.start()
            

    def stop(self,cam):
        if(self.calledFrom == 'auto'):
            self.stop_threads.set()
            self.thread1.join()
            self.thread1 = None
            print("stopped auto")
            self.system.busy = False
            self.system.GUI.updateStatusText()
            self.system.GUI.updateStatusBorder()
            
        if(self.calledFrom == 'focus'):
                self.stop_threads.set()
                self.thread3.join()
                self.thread3 = None
                print("stopped autofocus")
                self.system.busy = False
                self.system.GUI.updateStatusText()
                self.system.GUI.updateStatusBorder()
        if(cam==True):
            self.system.GUI.videoPower()
#             self.stop_threads.set()
#             print("stopped video")
#             self.system.busy = False
#             self.system.GUI.updateStatusText()
#             self.system.GUI.updateStatusBorder()
#             self.system.cam.vidPowerCnt +=1
            
        
#         try:
#             
#             if(self.calledFrom == 'auto'):
#                 self.stop_threads.set()
#                 self.thread1.join()
#                 self.thread1 = None
#                 print("stopped auto")
# 
#         except:
#             print("error: either autostart hasn't been pressed or automatic thread could not be stopped")
#             
#             try:
#                 
#                 
#                 if(self.calledFrom == 'focus'):
#                     self.stop_threads.set()
#                     self.thread1.join()
#                     self.thread1 = None
#                     print("stopped auto")
#                 
#             except:
#                 print("error: either autofocus hasn't been pressed or autofocus thread could not be stopped")
                
                
#         cnt++
