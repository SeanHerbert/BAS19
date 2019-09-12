import subprocess
from xlwt import Workbook


class Utility:
    def __init__(self):
        self.minPathology = 0
        self.maxPathology = 0
    def setPathology(self, min, max):
        self.minPathology = min
        self.maxPathology = max
    def dataEnter(self,fname ="ex.xls"):
        self.fname= fname
        self.wb = Workbook()
        self.s1 = self.wb.add_sheet("Sheet1")
        self.wb.save(self.fname)
        subprocess.Popen(['xdg-open',self.fname])
        

    
    