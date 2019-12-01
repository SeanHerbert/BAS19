from Utility import Utility
from Automatic import Automatic
from Focus import Focus
from carousel import carousel
from Illuminator import Illuminator
from BloodCounter import BloodCounter
from Manual import Manual
from FileHandler import FileHandler
from Controller import Controller
from Camera import Camera



class System():
    def __init__(self,GUI):
        
        self.GUI = GUI
        self.directory ="/home/pi/BAS/DataFiles/"
        self.dataFilePaths =[]
        self.currFileIndex = -1
        self.currImage = 0
        self.currImage_analyze = 0
        self.imgChange = False
        self.fileHandler = FileHandler(self)
        self.focus = Focus(self)
#         self.focus = Thread(target = Focus(self))
        self.carousel = carousel(self)
        self.illuminator =Illuminator(14,15,31)
        self.bloodCounter = BloodCounter(self)
        self.util = Utility(self)
        self.auto = Automatic(self)
        self.control = Controller(self)
        self.man = Manual(self)
        self.cam = Camera(self)
#         self.cam.setAperture(11)
        self.videoThreadStarted = False
        self.busy = False
#         self.video_getter = VideoGet(self)
#         self.video_shower = VideoShow(self.video_getter.frame,self)
    
    