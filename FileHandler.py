import subprocess
from openpyxl import Workbook
from openpyxl import load_workbook

from openpyxl.styles import Alignment
import os #was os.path 
from datetime import datetime
import time
from DataFileControl import DataFileControl
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')



class FileHandler():
    def __init__(self,usedIn):
        if(str(type(usedIn))!="<class 'System.System'>"):
            self.system = usedIn.system
        else:
            self.system = usedIn

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
        ws1.sheet_view.zoomScale = 225
        wb.save(path)
        self.system.currFileIndex += 1
    def openCurrentDataFile(self):
        if(len(self.system.dataFilePaths)>0):
            subprocess.Popen(['xdg-open', self.system.dataFilePaths[self.system.currFileIndex]])
            
            time.sleep(2)
            r = Tk()
            r.geometry("400x150+1520+0")
            r.call('wm', 'attributes', '.', '-topmost', '1') #keeps the keypad on top
            r.title("Save/Close")
            
            dfc = DataFileControl(r,self.system)
            dfc.grid()
            

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
    def readSampleID(self):
        if(len(self.system.dataFilePaths)>0):
            wb = load_workbook(self.system.dataFilePaths[self.system.currFileIndex])
            ws1 = wb.active
            sampleID = ws1.cell(row=self.system.carousel.curPos+1 ,column = 2).value
            print("current Carousel Position is: ",self.system.carousel.curPos )
            print(type(sampleID))
            return sampleID
        else:
            return None
        
    def reSizeCells(self, ws1):
        ws1.column_dimensions['A'].width= 15
        ws1.column_dimensions['B'].width= 10
        ws1.column_dimensions['C'].width= 12
        ws1.column_dimensions['D'].width= 14
        ws1.column_dimensions['E'].width= 14
        ws1.column_dimensions['F'].width= 14
        ws1.column_dimensions['G'].width= 10

    def centerText(self,ws1):
        for col in ws1.columns:
            for cell in col:
            # openpyxl styles aren't mutable,
            # so you have to create a copy of the style, modify the copy, then set it back
                alignment_obj = cell.alignment.copy(horizontal='center', vertical='center')
                cell.alignment = alignment_obj
