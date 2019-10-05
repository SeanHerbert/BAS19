from Utility import Utility
from Automatic import Automatic
from Focus import Focus
from carousel import carousel
from Illuminator import Illuminator
from BloodCounter import BloodCounter
from Manual import Manual
from tkinter import BOTH, END, LEFT
from FileHandler import FileHandler


class System():
    def __init__(self,GUI):
        self.GUI = GUI
        self.directory ="/home/pi/BAS/DataFiles/"
        self.dataFilePaths =[]
        self.currFileIndex = -1
        self.currImage = 0
        self.fileHandler = FileHandler(self)
        self.focus = Focus(self)
        self.carousel = carousel()
        self.illuminator =Illuminator(14,15,31)
        self.bloodCounter = BloodCounter()
        self.util = Utility(self)
        self.auto = Automatic(self)
        self.man = Manual(self)
    
    