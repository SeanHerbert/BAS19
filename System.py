from Utility import Utility
from Automatic import Automatic
class System():
    def __init__(self):
        self.directory ="/home/pi/BAS/DataFiles/"
        self.dataFilePaths =[]
        self.currFileIndex = -1
        
        self.util = Utility(self)

        self.auto = Automatic(self)
   