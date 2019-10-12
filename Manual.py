from FileHandler import FileHandler
    
class Manual():
    
    def __init__(self,system):
        self.system = system
        self.fileHandler = FileHandler(self)
        self.bloodData = []
    
    def countBlood(self):
        rbc = self.system.bloodCounter.countRBC(self.system.currImage)
        wbc = self.system.bloodCounter.countWBC(self.system.currImage)
        ratio = self.system.bloodCounter.calcRatio()
        self.bloodData = [wbc,rbc,ratio]
        return self.bloodData
    def saveData(self):
        self.fileHandler.writeRatio((self.system.carousel.curPos+1),self.bloodData[2])
    def captureImage(self):
        print("Image Captured")
        #will call Camera API here
#         self.system.currImage = cv2.imread(Image)
        #return self.system.currImage
        
        
        
        
    
        