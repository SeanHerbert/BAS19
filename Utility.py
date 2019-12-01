from FileHandler import FileHandler

class Utility():
    def __init__(self,system):
        self.system = system
        self.minPathology = -9999
        self.maxPathology = 9999
        self.fileHandler = FileHandler(self)
    def setPathology(self, min, max):
        self.minPathology = min
        self.maxPathology = max
    def pathologyWarn(self, bloodRatio):
        if((bloodRatio<self.minPathology) or (bloodRatio>self.maxPathology)):
            return True
        else:
            return False
    def createFile(self):
        self.fileHandler.createNewDataFile()
    def openCurrFile(self):
        self.fileHandler.openCurrentDataFile()
            

    
    