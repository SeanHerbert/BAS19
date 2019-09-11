
from openpyxl import Workbook
from openpyxl import load_workbook
import os


class Utility:
    def __init__(self):
        self.minPathology = 0
        self.maxPathology = 0
    def setPathology(self, min, max):
        self.minPathology = min
        self.maxPathology = max
    def dataEnter(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'newFile'
        self.filename = 'newFile.xlsx'
        self.df = 'DataFiles\\'
        self.path = self.df + self.filename
        self.wb.save(self.path)
        os.startfile(self.path)



    
    