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

#this class contains all the high level objects for system operation

class System():
    def __init__(self,GUI):
        
        #flags
        self.imgChange = False
        self.videoThreadStarted = False
        self.busy = False
        
        #storage variables accessible throughout BAS
        self.directory ="/home/pi/BAS/DataFiles/"
        self.dataFilePaths =[]
        self.currFileIndex = -1
        self.currImage = 0
        self.currImage_analyze = 0
        
        #Objects for system functionality (all but GUI and Illuminator get passed the system object
        #so they can talk to eachother 
        self.GUI = GUI
        self.fileHandler = FileHandler(self)#for file IO
        self.focus = Focus(self)#for controlling focus
        self.carousel = carousel(self)#for moving carousel
        self.illuminator =Illuminator(14,15,5)#for controlling LED
        self.bloodCounter = BloodCounter(self)#for analyzing blood 
        self.util = Utility(self)#for saving data and 
        self.auto = Automatic(self)#for utility frame controls
        self.control = Controller(self)#for handling threads
        self.man = Manual(self)#for manual frame controls 
        self.cam = Camera(self)#for controlling the camera
        

    
    