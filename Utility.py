from FileHandler import FileHandler

#THis class sets pathology, creates a new data file, and opens current data file 

class Utility():
    #constructor gets system object and Filehandler
    def __init__(self,system):
        self.system = system
        self.minPathology = -9999
        self.maxPathology = 9999
        self.fileHandler = FileHandler(self)
        
    #set pathology 
    def setPathology(self, min, max):
        self.minPathology = min
        self.maxPathology = max
        
    #returns true or false if pathoplogy is out of range or in range
    def pathologyWarn(self, bloodRatio):
        if((bloodRatio<self.minPathology) or (bloodRatio>self.maxPathology)):
            return True
        else:
            return False
    
    #creates a new Datafile
    def createFile(self):
        self.fileHandler.createNewDataFile()
        
    #opens current datafile
    def openCurrFile(self):
        self.fileHandler.openCurrentDataFile()
            

    
    