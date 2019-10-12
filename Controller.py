from threading import Thread,Event

class Controller(object):
    def __init__(self,system):
        self.thread1 = None
        self.thread2 = None
        self.stop_threads = Event()
        self.system = system

    def loop1(self):
        
        while not self.stop_threads.is_set():
            x = self.system.auto.start()
#             if x=='done':
#                 self.stop()
        self.stop_threads.clear()
        
            
#     def loop2(self):
#         while not self.stop_threads.is_set():
#             x=3

    def combine(self):
        if(len(self.system.dataFilePaths)==0):
            self.system.util.createFile()
        self.stop_threads.clear()
        self.thread1 = Thread(target = self.loop1)
#         self.thread2 = Thread(target = self.loop2)
        self.thread1.start()
#         self.thread2.start()

    def stop(self):
        self.stop_threads.set()
        self.thread1.join()
#         self.thread2.join()
        self.thread1 = None
#         self.thread2 = None