from threading import Thread,Event
from openpyxl import load_workbook

class Controller(object):
    def __init__(self,system):
        self.thread1 = None
        self.thread2 = None
        self.stop_threads = Event()
        self.system = system

    def loop1(self):
        
        while not self.stop_threads.is_set():
            x = self.system.auto.start()
            if x=='done':
                break
        self.stop_threads.clear()
        
            
#     def loop2(self):
#         while not self.stop_threads.is_set():
#             x=3

    def combine(self):
        if(len(self.system.dataFilePaths)==0):
            self.system.util.createFile()
        self.wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
        self.ws1 = self.wb.active
        self.stop_threads.clear()
        self.thread1 = Thread(target = self.loop1)
#         self.thread2 = Thread(target = self.loop2)
        self.thread1.start()
#         self.thread2.start()

    def stop(self):
        try:
            self.stop_threads.set()
            self.thread1.join()
    #         self.thread2.join()
            self.thread1 = None
#         self.thread2 = None
        except:
            print("error: either autostart hasn't been pressed or automatic thread could not be stopped")
