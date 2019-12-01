from ximea import xiapi

from threading import Thread
import cv2

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self,system):
        self.system = system
        self.frame =None
        self.img = xiapi.Image()
#         self.img = xiapi.Image()
#         self.system.cam.cam.get_image(self.img,100000)
#         self.frame = self.img.get_image_data_numpy()
        
        self.stopped = False

    def start(self):
        self.stopped = False
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            self.system.cam.cam.get_image(self.img,100000)
            self.frame = self.img.get_image_data_numpy()
            
            

    def stop(self):
        self.stopped = True
        self.cam.stop_acquisition()