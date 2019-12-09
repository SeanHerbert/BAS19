from threading import Thread,Event
from openpyxl import load_workbook
import numpy as np 

#this class controls most threading for the BAS
#It has an Event object that sets a stop flag when stop is called
#autostart, video, and autofocus are cotrolled through this class 

class Controller(object):
    
    #constructor gets system object 
    def __init__(self,system):
        self.thread1 = None
        self.thread2 = None
        self.thread3 = None
        self.stop_threads = Event()
        self.system = system
        
    #loop1 targets autostart 
    def loop1(self):
        while not self.stop_threads.is_set():
            x = self.system.auto.start()
            if x=='done':
                self.system.GUI.queue.put("setReady")
                self.stop_threads.clear()
                return
        
    #loop2 targets video. Video thread is unqiue, because it is never killed once started
    #(had to be that way due to cv2.imshow threading complications)        
    def loop2(self):
        self.system.videoThreadStarted = True # set video started flag
        while True:
            self.system.cam.startVideo() # runs thread indefinitely
        self.stop_threads.clear()
    
    #loop3 targets autoFocus
    def loop3(self):
        while not self.stop_threads.is_set():
            x=self.system.focus.autoFocus()
            if(isinstance(x, (np.ndarray))):
                self.system.GUI.queue.put("setReady")
                self.stop_threads.clear()
                return
            
        
        

    #starts the threads based on calledFrom param (should probably rename to startThread or something
    def combine(self,calledFrom):
        self.calledFrom =calledFrom
        
        #start auto thread
        if(self.calledFrom == 'auto'):
            self.system.GUI.updateStatusText("Automatic")
            self.system.GUI.updateStatusBorder("yellow")
            self.system.busy = True
            
            #had to put the datafile stuff in the following block here because of threading complications
            if(len(self.system.dataFilePaths)==0):
                self.system.util.createFile()
            self.wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
            self.ws1 = self.wb.active
            
            self.stop_threads.clear()
            self.thread1 = Thread(target = self.loop1)
            self.thread1.start()
        
        #start video thread
        if(self.calledFrom =='cam'):
            self.stop_threads.clear()
            if(self.system.videoThreadStarted == False):
                self.thread2 = Thread(target = self.loop2)
                self.thread2.start()
        
        #start autofocus thread 
        if(self.calledFrom == 'focus'):
            self.system.GUI.updateStatusText("Autofocusing")
            self.system.GUI.updateStatusBorder("yellow")
            self.system.busy = True
            self.stop_threads.clear()
            self.thread3 = Thread(target=self.loop3)
            self.thread3.start()
            
    #stops threads based on calledFrom param. Special cam param for camera stop.
    def stop(self,cam):
        
        #kill automatic thread 
        if(self.calledFrom == 'auto'):
            self.stop_threads.set()
            self.thread1.join()
            self.thread1 = None
            print("stopped auto")
            self.system.busy = False
            self.system.GUI.updateStatusText()
            self.system.GUI.updateStatusBorder()
        
        #kill autofocus thread
        if(self.calledFrom == 'focus'):
            self.stop_threads.set()
            self.thread3.join()
            self.thread3 = None
            print("stopped autofocus")
            self.system.busy = False
            self.system.GUI.updateStatusText()
            self.system.GUI.updateStatusBorder()
        
        #stop video(notice no thread kill)
        if(cam==True):
            self.system.GUI.videoPower()
            print("stopped video")

