from threading import Thread,Event
from subprocess import call

class Controller(object):
    def __init__(self,auto):
        self.thread1 = None
        self.thread2 = None
        self.stop_threads = Event()
        self.auto = auto

    def loop1(self):
        while not self.stop_threads.is_set():
            self.auto.start()
            
#             call (["raspivid -n -op 150 -w 640 -h 480 -b 2666666.67 -t 5000 -o test.mp4"],shell=True)
#             call (["raspivid -n -op 150 -w 640 -h 480 -b 2666666.67 -t 5000 -o test1.mp4"],shell=True)

#     def loop2(self):
#         while not self.stop_threads.is_set():
#             x=3

    def combine(self):
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