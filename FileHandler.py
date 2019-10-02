import subprocess
from openpyxl import Workbook
from openpyxl import load_workbook

from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import os.path 
from datetime import datetime

class FileHandler():
    def __init__(self,usedIn):
        self.system = usedIn.system
    #     self.system.directory = usedIn.directory
    #     self.system.dataFilePaths=usedIn.dataFilePaths
    #     self.system.currFileIndex = usedIn.currFileIndex
    def createNewDataFile(self):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y:%H:%M:%S")
        fname= "bloodcount_"+dt_string+".xlsx"
        path = self.system.directory+fname
        self.system.dataFilePaths.append(path)
        wb = Workbook()
        ws1 = wb.active
        ws1.title = "bloodcount"
        self.writeBoilerPlate(ws1)
        self.reSizeCells(ws1)
        self.centerText(ws1)
        wb.save(path)
        self.system.currFileIndex += 1
    def openCurrentDataFile(self):
        if(len(self.system.dataFilePaths)>=0):
            subprocess.Popen(['xdg-open',self.system.dataFilePaths[self.system.currFileIndex]])
    def writeBoilerPlate(self,ws1):
        header = [u'Slide Position', u'Sample ID', u'Sample Date',
                    u'Analysis Date',u'Analysis Time',
                    u'WBC/RBC Ratio', u'Pathology']
        ws1.append(header)
        for i in range (1,21):
            ws1.cell(row=i+1, column=1, value=i)
    def writeRatio(self,index,ratio):
        if(len(self.system.dataFilePaths)>0):
            wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
            ws1 = wb.active
            ws1.cell(row=index+2, column=6, value= ratio)

        else:
            self.createNewDataFile()
            wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
            ws1 = wb.active
            ws1.cell(row=index+2, column=6, value= ratio)
        wb.save(self.system.dataFilePaths[self.system.currFileIndex])
        
            
    def reSizeCells(self, ws1):
        column_widths = []
        for row in ws1.rows:
            for i, cell in enumerate(row):
                if len(column_widths) > i:
                    if len(str(cell.value)) > column_widths[i]:
                        column_widths[i] = len(str(cell.value))
                else:
                    column_widths += [len(str(cell.value))]

        for i, column_width in enumerate(column_widths):
            ws1.column_dimensions[get_column_letter(i+1)].width= column_width+1
    def centerText(self,ws1):
        for col in ws1.columns:
            for cell in col:
            # openpyxl styles aren't mutable,
            # so you have to create a copy of the style, modify the copy, then set it back
                alignment_obj = cell.alignment.copy(horizontal='center', vertical='center')
                cell.alignment = alignment_obj
