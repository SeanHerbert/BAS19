import subprocess
from xlwt import Workbook


class Utility:
    def __init__(self):
        self.minPathology = 0
        self.maxPathology = 0
    def setPathology(self, min, max):
        self.minPathology = min
        self.maxPathology = max
    def dataEnter(self,fname ="dataFile.xls"):
        self.fname= fname
        self.dir ="/home/pi/BAS/DataFiles/"
        self.path = self.dir+self.fname
        self.wb = Workbook()
        self.s1 = self.wb.add_sheet("Sheet1")
        self.wb.save(self.path)
        subprocess.Popen(['xdg-open',self.path])
    
        
        

    
    