

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import GUI_support

from System import System
from Focus import Focus
from BloodCounter import BloodCounter
from tkinter import *
from PIL import ImageTk, Image
from KeyPad import KeyPad
from datetime import datetime

# 

   




def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    GUI_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    BASGUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
     
    def jogDwn(self):
        self.system.focus.jogDown()
        self.focusPosText.delete("1.0", "end")
        self.focusPosText.insert(END,self.system.focus.zVar())
       
    def jogUp(self):
        self.system.focus.jogUp()
        self.focusPosText.delete("1.0", "end")
        self.focusPosText.insert(END,self.system.focus.zVar())
        
    def autoFocus(self):
        self.system.focus.autoFocus()
        self.focusPosText.delete("1.0", "end")
        self.focusPosText.insert(END,self.system.focus.zVar())
    
    def countBlood(self):
        self.sampleRatioText.configure(highlightthickness=0)
        self.system.man.countBlood()
        self.sampleBloodCountText.delete("1.0", "end")
        self.sampleBloodCountText.insert(END,"{}/{}".format(self.system.man.bloodData[0], self.system.man.bloodData[1]))
        self.sampleRatioText.delete("1.0", "end")
        self.sampleRatioText.insert(END,self.system.bloodCounter.ratio)
        
            
    
    def saveData(self):
        self.system.man.saveData()
   
    def createFile(self):
        self.system.util.createFile()
    
    def openFile(self):
        self.system.util.openCurrFile()
  
    def setPathology(self):
        self.system.util.setPathology(self.minPathologyText.get("1.0",END),self.maxPathologyText.get("1.0",END))
    
    def autoStart(self):
        self.sampleRatioText.configure(highlightthickness=0)
        self.system.control.combine()
    def eStop(self):
        self.system.control.stop()
      
    def ledPower(self):
        
            
        if(self.ledPowerCnt % 2 == 0):
            self.system.illuminator.turnOn()
            if(self.ledPowerCnt==0):
                self.system.illuminator.turnOff()
                self.system.illuminator.turnOn()
        else:
            self.system.illuminator.turnOff()
        self.ledPowerCnt +=1
        
    def setLed(self):
        self.system.illuminator.changeColor(int(self.redLevelText.get("1.0",END)),int(self.greenLevelText.get("1.0",END)),int(self.blueLevelText.get("1.0",END)))
        
    def ccwStep(self):
        self.system.carousel.stepForward()
        
    def cwStep(self):
        self.system.carousel.stepBackward()
        
    def zeroCarousel(self):
        self.system.carousel.zeroPos()
        
    def goToSlide(self):
        self.system.carousel.moveToSlide(int(self.goToSlideText.get("1.0",END)))
        self.sampleIdText.delete("1.0","end")
        if(self.system.fileHandler.readSampleID()!= None):
            self.sampleIdText.insert(END,self.system.fileHandler.readSampleID())
    
    def genKeyPad(self,event):
        if(self.kpRunning==0):
            r = Tk()
            r.call('wm', 'attributes', '.', '-topmost', '1') #keeps the keypad on top
            caller = event.widget
            r.title("Keypad")
            
            kp = KeyPad(r,self,caller)
            kp.grid()
            
        
            

 
        
        
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font25 = "-family {Segoe UI} -size 25 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font20 = "-family {Segoe UI} -size 20 -slant roman "  \
            "-underline 0 -overstrike 0"

        top.geometry("1920x1060+-1+0")
        top.title("Blood Analyzer")
        top.configure(background="#d9d9d9")
        
        self.ledPowerCnt = 0
        self.kpRunning = 0
        self.healthStatusFrame = tk.LabelFrame(top)
        self.healthStatusFrame.place(relx=0.006, rely=0.0, relheight=0.16
                , relwidth=0.192)
        self.healthStatusFrame.configure(relief='groove')
        self.healthStatusFrame.configure(borderwidth="8")
        self.healthStatusFrame.configure(font=font25)
        self.healthStatusFrame.configure(foreground="black")
        self.healthStatusFrame.configure(text='''Health/Status''')
        self.healthStatusFrame.configure(background="#d9d9d9")

        self.statusText = tk.Text(self.healthStatusFrame)
        self.statusText.place(relx=0.062, rely=0.275, relheight=0.282, relwidth=0.622
                , bordermode='ignore')
        self.statusText.configure(background="white")
        self.statusText.configure(font=font20)
        self.statusText.configure(foreground="black")
        self.statusText.configure(highlightbackground="#d9d9d9")
        self.statusText.configure(highlightcolor="black")
        self.statusText.configure(insertbackground="black")
        self.statusText.configure(selectbackground="#c4c4c4")
        self.statusText.configure(selectforeground="black")
        self.statusText.configure(wrap="word")

        self.camTempText = tk.Text(self.healthStatusFrame)
        self.camTempText.place(relx=0.064, rely=0.61, relheight=0.282
                , relwidth=0.211, bordermode='ignore')
        self.camTempText.configure(background="white")
        self.camTempText.configure(font=font20)
        self.camTempText.configure(foreground="black")
        self.camTempText.configure(highlightbackground="#d9d9d9")
        self.camTempText.configure(highlightcolor="black")
        self.camTempText.configure(insertbackground="black")
        self.camTempText.configure(selectbackground="#c4c4c4")
        self.camTempText.configure(selectforeground="black")
        self.camTempText.configure(wrap="word")

        self.camTempLabel = tk.Label(self.healthStatusFrame)
        self.camTempLabel.place(relx=0.32, rely=0.688, height=26, width=220
                , bordermode='ignore')
        self.camTempLabel.configure(font=font20)

        self.camTempLabel.configure(background="#d9d9d9")
        self.camTempLabel.configure(disabledforeground="#a3a3a3")
        self.camTempLabel.configure(foreground="#000000")
        self.camTempLabel.configure(text='''Cam Temp (°C)''')

        self.cameraFrame = tk.LabelFrame(top)
        self.cameraFrame.place(relx=0.202, rely=0.39, relheight=0.12
                , relwidth=0.192)
        self.cameraFrame.configure(relief='groove')
        self.cameraFrame.configure(borderwidth="8")
        self.cameraFrame.configure(font=font25)
        self.cameraFrame.configure(foreground="black")
        self.cameraFrame.configure(text='''Camera''')
        self.cameraFrame.configure(background="#d9d9d9")
        self.cameraFrame.configure(highlightbackground="#d9d9d9")
        self.cameraFrame.configure(highlightcolor="black")

        self.camAdjustButton = tk.Button(self.cameraFrame)
        self.camAdjustButton.place(relx=0.062, rely=0.308, height=64, width=300
                , bordermode='ignore')
        self.camAdjustButton.configure(activebackground="#ececec")
        self.camAdjustButton.configure(activeforeground="#000000")
        self.camAdjustButton.configure(background="#b7b7b7")
        self.camAdjustButton.configure(disabledforeground="#a3a3a3")
        self.camAdjustButton.configure(foreground="#000000")
        self.camAdjustButton.configure(highlightbackground="#d9d9d9")
        self.camAdjustButton.configure(highlightcolor="black")
        self.camAdjustButton.configure(pady="0")
        self.camAdjustButton.configure(text='''Camera Adjust''')
        self.camAdjustButton.configure(font=font20)

        self.focusFrame = tk.LabelFrame(top)
        self.focusFrame.place(relx=0.202, rely=0.0, relheight=0.391
                , relwidth=0.192)
        self.focusFrame.configure(relief='groove')
        self.focusFrame.configure(borderwidth="8")
        self.focusFrame.configure(font=font25)
        self.focusFrame.configure(foreground="black")
        self.focusFrame.configure(text='''Focus''')
        self.focusFrame.configure(background="#d9d9d9")
        self.focusFrame.configure(highlightbackground="#d9d9d9")
        self.focusFrame.configure(highlightcolor="black")

        self.minusStepFocusButton = tk.Button(self.focusFrame)
        self.minusStepFocusButton.place(relx=0.062, rely=0.114, height=64, width=150
                , bordermode='ignore')
        self.minusStepFocusButton.configure(activebackground="#ececec")
        self.minusStepFocusButton.configure(activeforeground="#000000")
        self.minusStepFocusButton.configure(background="#b7b7b7")
        self.minusStepFocusButton.configure(disabledforeground="#a3a3a3")
        self.minusStepFocusButton.configure(foreground="#000000")
        self.minusStepFocusButton.configure(highlightbackground="#d9d9d9")
        self.minusStepFocusButton.configure(highlightcolor="black")
        self.minusStepFocusButton.configure(pady="0")
        self.minusStepFocusButton.configure(text='''Step(-)''')
        self.minusStepFocusButton.configure(command= self.jogDwn);
        self.minusStepFocusButton.configure(font=font20)
        
        
        

        self.plusStepFocusButton = tk.Button(self.focusFrame)
        self.plusStepFocusButton.place(relx=0.497, rely=0.114, height=64, width=150
                , bordermode='ignore')
        self.plusStepFocusButton.configure(activebackground="#ececec")
        self.plusStepFocusButton.configure(activeforeground="#000000")
        self.plusStepFocusButton.configure(background="#b7b7b7")
        self.plusStepFocusButton.configure(disabledforeground="#a3a3a3")
        self.plusStepFocusButton.configure(foreground="#000000")
        self.plusStepFocusButton.configure(highlightbackground="#d9d9d9")
        self.plusStepFocusButton.configure(highlightcolor="black")
        self.plusStepFocusButton.configure(pady="0")
        self.plusStepFocusButton.configure(text='''Step(+)''')
        self.plusStepFocusButton.configure(command= self.jogUp);
        self.plusStepFocusButton.configure(font=font20)


        self.focusPosText = tk.Text(self.focusFrame)
        self.focusPosText.place(relx=0.062, rely=0.343, relheight=0.137
                , relwidth=0.273, bordermode='ignore')
        self.focusPosText.configure(background="white")
        self.focusPosText.configure(font=font20)
        self.focusPosText.configure(foreground="black")
        self.focusPosText.configure(highlightbackground="#d9d9d9")
        self.focusPosText.configure(highlightcolor="black")
        self.focusPosText.configure(insertbackground="black")
        self.focusPosText.configure(selectbackground="#c4c4c4")
        self.focusPosText.configure(selectforeground="black")
        self.focusPosText.configure(wrap="word")
        self.focusPosText.insert(END,"10000")

        self.focusPosLabel = tk.Label(self.focusFrame)
        self.focusPosLabel.place(relx=0.352, rely=0.375, height=26, width=209
                , bordermode='ignore')
        self.focusPosLabel.configure(activebackground="#f9f9f9")
        self.focusPosLabel.configure(activeforeground="black")
        self.focusPosLabel.configure(background="#d9d9d9")
        self.focusPosLabel.configure(disabledforeground="#a3a3a3")
        self.focusPosLabel.configure(foreground="#000000")
        self.focusPosLabel.configure(highlightbackground="#d9d9d9")
        self.focusPosLabel.configure(highlightcolor="black")
        self.focusPosLabel.configure(text='''Focus pos (um)''')
        self.focusPosLabel.configure(font=font20)

        self.videoButton = tk.Button(self.focusFrame)
        self.videoButton.place(relx=0.062, rely=0.543, height=64, width=300
                , bordermode='ignore')
        self.videoButton.configure(activebackground="#ececec")
        self.videoButton.configure(activeforeground="#000000")
        self.videoButton.configure(background="#b7b7b7")
        self.videoButton.configure(disabledforeground="#a3a3a3")
        self.videoButton.configure(foreground="#000000")
        self.videoButton.configure(highlightbackground="#d9d9d9")
        self.videoButton.configure(highlightcolor="black")
        self.videoButton.configure(pady="0")
        self.videoButton.configure(text='''Video''')
        self.videoButton.configure(font=font20)
        
#         self.plusStepFocusButton.configure(command=lambda : self.turnOnVideo());


        self.autoFocusButton = tk.Button(self.focusFrame)
        self.autoFocusButton.place(relx=0.062, rely=0.743, height=64, width=300
                , bordermode='ignore')
        self.autoFocusButton.configure(activebackground="#ececec")
        self.autoFocusButton.configure(activeforeground="#000000")
        self.autoFocusButton.configure(background="#b7b7b7")
        self.autoFocusButton.configure(disabledforeground="#a3a3a3")
        self.autoFocusButton.configure(foreground="#000000")
        self.autoFocusButton.configure(highlightbackground="#d9d9d9")
        self.autoFocusButton.configure(highlightcolor="black")
        self.autoFocusButton.configure(pady="0")
        self.autoFocusButton.configure(text='''Auto Focus''')
        self.autoFocusButton.configure(command = self.autoFocus) #thread this and hook it to e-stop
        self.autoFocusButton.configure(font=font20)


        self.manualFrame = tk.LabelFrame(top)
        self.manualFrame.place(relx=0.396, rely=0.649, relheight=0.342
                , relwidth=0.192)
        self.manualFrame.configure(relief='groove')
        self.manualFrame.configure(borderwidth="8")
        self.manualFrame.configure(font=font25)
        self.manualFrame.configure(foreground="black")
        self.manualFrame.configure(text='''Manual''')
        self.manualFrame.configure(background="#d9d9d9")
        self.manualFrame.configure(highlightbackground="#d9d9d9")
        self.manualFrame.configure(highlightcolor="black")

        self.captureImageButton = tk.Button(self.manualFrame)
        self.captureImageButton.place(relx=0.062, rely=0.131, height=64, width=300
                , bordermode='ignore')
        self.captureImageButton.configure(activebackground="#ececec")
        self.captureImageButton.configure(activeforeground="#000000")
        self.captureImageButton.configure(background="#b7b7b7")
        self.captureImageButton.configure(disabledforeground="#a3a3a3")
        self.captureImageButton.configure(foreground="#000000")
        self.captureImageButton.configure(highlightbackground="#d9d9d9")
        self.captureImageButton.configure(highlightcolor="black")
        self.captureImageButton.configure(pady="0")
        self.captureImageButton.configure(text='''Capture image''')
        self.captureImageButton.configure(font=font20)
#         self.captureImageButton.configure(command=lambda : self.getImage());



        self.analyzeSampleButton = tk.Button(self.manualFrame)
        self.analyzeSampleButton.place(relx=0.062, rely=0.425, height=64, width=300
                , bordermode='ignore')
        self.analyzeSampleButton.configure(activebackground="#ececec")
        self.analyzeSampleButton.configure(activeforeground="#000000")
        self.analyzeSampleButton.configure(background="#b7b7b7")
        self.analyzeSampleButton.configure(disabledforeground="#a3a3a3")
        self.analyzeSampleButton.configure(foreground="#000000")
        self.analyzeSampleButton.configure(highlightbackground="#d9d9d9")
        self.analyzeSampleButton.configure(highlightcolor="black")
        self.analyzeSampleButton.configure(pady="0")
        self.analyzeSampleButton.configure(text='''Analyze sample''')
        self.analyzeSampleButton.configure(command= self.countBlood) #thread this, maybe have a kill command?
        self.analyzeSampleButton.configure(font=font20)

        self.saveDataButton = tk.Button(self.manualFrame)
        self.saveDataButton.place(relx=0.062, rely=0.719, height=64, width=300
                , bordermode='ignore')
        self.saveDataButton.configure(activebackground="#ececec")
        self.saveDataButton.configure(activeforeground="#000000")
        self.saveDataButton.configure(background="#b7b7b7")
        self.saveDataButton.configure(disabledforeground="#a3a3a3")
        self.saveDataButton.configure(foreground="#000000")
        self.saveDataButton.configure(highlightbackground="#d9d9d9")
        self.saveDataButton.configure(highlightcolor="black")
        self.saveDataButton.configure(pady="0")
        self.saveDataButton.configure(text='''Save data''')
        self.saveDataButton.configure(command = self.saveData)
        self.saveDataButton.configure(font=font20)

        self.utilityFrame = tk.LabelFrame(top)
        self.utilityFrame.place(relx=0.202, rely=0.515, relheight=0.47
                , relwidth=0.192)
        self.utilityFrame.configure(relief='groove')
        self.utilityFrame.configure(borderwidth="8")
        self.utilityFrame.configure(font=font25)
        self.utilityFrame.configure(foreground="black")
        self.utilityFrame.configure(text='''Utility''')
        self.utilityFrame.configure(background="#d9d9d9")
        self.utilityFrame.configure(highlightbackground="#d9d9d9")
        self.utilityFrame.configure(highlightcolor="black")

        self.createFileButton = tk.Button(self.utilityFrame)
        self.createFileButton.place(relx=0.062, rely=0.095, height=64, width=300
                , bordermode='ignore')
        self.createFileButton.configure(activebackground="#ececec")
        self.createFileButton.configure(activeforeground="#000000")
        self.createFileButton.configure(background="#b7b7b7")
        self.createFileButton.configure(disabledforeground="#a3a3a3")
        self.createFileButton.configure(foreground="#000000")
        self.createFileButton.configure(highlightbackground="#d9d9d9")
        self.createFileButton.configure(highlightcolor="black")
        self.createFileButton.configure(pady="0")
        self.createFileButton.configure(text='''Create file''')
        self.createFileButton.configure(command= self.createFile)
        self.createFileButton.configure(font=font20)


        self.openFileButton = tk.Button(self.utilityFrame)
        self.openFileButton.place(relx=0.062, rely=0.31, height=64, width=300
                , bordermode='ignore')
        self.openFileButton.configure(activebackground="#ececec")
        self.openFileButton.configure(activeforeground="#000000")
        self.openFileButton.configure(background="#b7b7b7")
        self.openFileButton.configure(disabledforeground="#a3a3a3")
        self.openFileButton.configure(foreground="#000000")
        self.openFileButton.configure(highlightbackground="#d9d9d9")
        self.openFileButton.configure(highlightcolor="black")
        self.openFileButton.configure(pady="0")
        self.openFileButton.configure(text='''Open file''')
        self.openFileButton.configure(command = self.openFile)
        self.openFileButton.configure(font=font20)

        self.setPathologyButton = tk.Button(self.utilityFrame)
        self.setPathologyButton.place(relx=0.062, rely=0.524, height=64, width=300
                , bordermode='ignore')
        self.setPathologyButton.configure(activebackground="#ececec")
        self.setPathologyButton.configure(activeforeground="#000000")
        self.setPathologyButton.configure(background="#b7b7b7")
        self.setPathologyButton.configure(disabledforeground="#a3a3a3")
        self.setPathologyButton.configure(foreground="#000000")
        self.setPathologyButton.configure(highlightbackground="#d9d9d9")
        self.setPathologyButton.configure(highlightcolor="black")
        self.setPathologyButton.configure(pady="0")
        self.setPathologyButton.configure(text='''Set pathology''')
        self.setPathologyButton.configure(command = self.setPathology)
        self.setPathologyButton.configure(font=font20)

        self.minPathologyText = tk.Text(self.utilityFrame)
        self.minPathologyText.place(relx=0.062, rely=0.786, relheight=0.152
                , relwidth=0.335, bordermode='ignore')
        self.minPathologyText.configure(background="white")
        self.minPathologyText.configure(font=font20)
        self.minPathologyText.configure(foreground="black")
        self.minPathologyText.configure(highlightbackground="#d9d9d9")
        self.minPathologyText.configure(highlightcolor="black")
        self.minPathologyText.configure(insertbackground="black")
        self.minPathologyText.configure(selectbackground="#c4c4c4")
        self.minPathologyText.configure(selectforeground="black")
        self.minPathologyText.configure(wrap="word")
        self.minPathologyText.bind("<Button-1>",lambda e: self.genKeyPad(e))

        self.maxPathologyText = tk.Text(self.utilityFrame)
        self.maxPathologyText.place(relx=0.528, rely=0.786, relheight=0.152
                , relwidth=0.335, bordermode='ignore')
        self.maxPathologyText.configure(background="white")
        self.maxPathologyText.configure(font=font20)
        self.maxPathologyText.configure(foreground="black")
        self.maxPathologyText.configure(highlightbackground="#d9d9d9")
        self.maxPathologyText.configure(highlightcolor="black")
        self.maxPathologyText.configure(insertbackground="black")
        self.maxPathologyText.configure(selectbackground="#c4c4c4")
        self.maxPathologyText.configure(selectforeground="black")
        self.maxPathologyText.configure(wrap="word")
        self.maxPathologyText.bind("<Button-1>",lambda e: self.genKeyPad(e))

        self.minPathologyLabel = tk.Label(self.utilityFrame)
        self.minPathologyLabel.place(relx=0.124, rely=0.714, height=25, width=70
                , bordermode='ignore')
        self.minPathologyLabel.configure(background="#d9d9d9")
        self.minPathologyLabel.configure(disabledforeground="#a3a3a3")
        self.minPathologyLabel.configure(foreground="#000000")
        self.minPathologyLabel.configure(text='''Min''')
        self.minPathologyLabel.configure(font=font20)

        self.maxPathologyLabel = tk.Label(self.utilityFrame)
        self.maxPathologyLabel.place(relx=0.559, rely=0.714, height=25, width=70
                , bordermode='ignore')
        self.maxPathologyLabel.configure(activebackground="#f9f9f9")
        self.maxPathologyLabel.configure(activeforeground="black")
        self.maxPathologyLabel.configure(background="#d9d9d9")
        self.maxPathologyLabel.configure(disabledforeground="#a3a3a3")
        self.maxPathologyLabel.configure(foreground="#000000")
        self.maxPathologyLabel.configure(highlightbackground="#d9d9d9")
        self.maxPathologyLabel.configure(highlightcolor="black")
        self.maxPathologyLabel.configure(text='''Max''')
        self.maxPathologyLabel.configure(font=font20)

        self.automaticFrame = tk.LabelFrame(top)
        self.automaticFrame.place(relx=0.592, rely=0.649, relheight=0.342
                , relwidth=0.192)
        self.automaticFrame.configure(relief='groove')
        self.automaticFrame.configure(borderwidth="8")
        self.automaticFrame.configure(font=font25)
        self.automaticFrame.configure(foreground="black")
        self.automaticFrame.configure(text='''Automatic''')
        self.automaticFrame.configure(background="#d9d9d9")
        self.automaticFrame.configure(highlightbackground="#d9d9d9")
        self.automaticFrame.configure(highlightcolor="black")

        self.autoStartButton = tk.Button(self.automaticFrame)
        self.autoStartButton.place(relx=0.062, rely=0.131, height=64, width=300
                , bordermode='ignore')
        self.autoStartButton.configure(activebackground="#ececec")
        self.autoStartButton.configure(activeforeground="#000000")
        self.autoStartButton.configure(background="#b7b7b7")
        self.autoStartButton.configure(disabledforeground="#a3a3a3")
        self.autoStartButton.configure(foreground="#000000")
        self.autoStartButton.configure(highlightbackground="#d9d9d9")
        self.autoStartButton.configure(highlightcolor="black")
        self.autoStartButton.configure(pady="0")
        self.autoStartButton.configure(text='''Start''')
        self.autoStartButton.configure(command= self.autoStart)
        self.autoStartButton.configure(font=font20)


        self.emergencyStopButton = tk.Button(self.automaticFrame)
        self.emergencyStopButton.place(relx=0.062, rely=0.49, height=160, width=300
                , bordermode='ignore')
        self.emergencyStopButton.configure(activebackground="#ececec")
        self.emergencyStopButton.configure(activeforeground="#000000")
        self.emergencyStopButton.configure(background="#ff0000")
        self.emergencyStopButton.configure(disabledforeground="#a3a3a3")
        self.emergencyStopButton.configure(font=font20)
        self.emergencyStopButton.configure(foreground="#000000")
        self.emergencyStopButton.configure(highlightbackground="#d9d9d9")
        self.emergencyStopButton.configure(highlightcolor="black")
        self.emergencyStopButton.configure(pady="0")
        self.emergencyStopButton.configure(text='''Emergency stop''')
        self.emergencyStopButton.configure(command= self.eStop)

        self.illuminatorFrame = tk.LabelFrame(top)
        self.illuminatorFrame.place(relx=0.006, rely=0.159, relheight=0.483
                , relwidth=0.192)
        self.illuminatorFrame.configure(relief='groove')
        self.illuminatorFrame.configure(borderwidth="8")
        self.illuminatorFrame.configure(font=font25)
        self.illuminatorFrame.configure(foreground="black")
        self.illuminatorFrame.configure(text='''Illuminator''')
        self.illuminatorFrame.configure(background="#d9d9d9")
        self.illuminatorFrame.configure(highlightbackground="#d9d9d9")
        self.illuminatorFrame.configure(highlightcolor="black")

        self.ledPowerButton = tk.Button(self.illuminatorFrame)
        self.ledPowerButton.place(relx=0.062, rely=0.093, height=64, width=300
                , bordermode='ignore')
        self.ledPowerButton.configure(activebackground="#757575")
        self.ledPowerButton.configure(activeforeground="white")
        self.ledPowerButton.configure(activeforeground="#000000")
        self.ledPowerButton.configure(background="#b7b7b7")
        self.ledPowerButton.configure(disabledforeground="#a3a3a3")
        self.ledPowerButton.configure(foreground="#000000")
        self.ledPowerButton.configure(highlightbackground="#d9d9d9")
        self.ledPowerButton.configure(highlightcolor="black")
        self.ledPowerButton.configure(pady="0")
        self.ledPowerButton.configure(text='''Power''')
        self.ledPowerButton.configure(command= self.ledPower)
        self.ledPowerButton.configure(font=font20)


        self.redLevelText = tk.Text(self.illuminatorFrame)
        self.redLevelText.place(relx=0.062, rely=0.278, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.redLevelText.configure(background="white")
        self.redLevelText.configure(font=font20)
        self.redLevelText.configure(foreground="black")
        self.redLevelText.configure(highlightbackground="#d9d9d9")
        self.redLevelText.configure(highlightcolor="black")
        self.redLevelText.configure(insertbackground="black")
        self.redLevelText.configure(selectbackground="#c4c4c4")
        self.redLevelText.configure(selectforeground="black")
        self.redLevelText.configure(wrap="word")
        self.redLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))

        self.greenLevelText = tk.Text(self.illuminatorFrame)
        self.greenLevelText.place(relx=0.062, rely=0.463, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.greenLevelText.configure(background="white")
        self.greenLevelText.configure(font=font20)
        self.greenLevelText.configure(foreground="black")
        self.greenLevelText.configure(highlightbackground="#d9d9d9")
        self.greenLevelText.configure(highlightcolor="black")
        self.greenLevelText.configure(insertbackground="black")
        self.greenLevelText.configure(selectbackground="#c4c4c4")
        self.greenLevelText.configure(selectforeground="black")
        self.greenLevelText.configure(wrap="word")
        self.greenLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))

        self.blueLevelText = tk.Text(self.illuminatorFrame)
        self.blueLevelText.place(relx=0.062, rely=0.648, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.blueLevelText.configure(background="white")
        self.blueLevelText.configure(font=font20)
        self.blueLevelText.configure(foreground="black")
        self.blueLevelText.configure(highlightbackground="#d9d9d9")
        self.blueLevelText.configure(highlightcolor="black")
        self.blueLevelText.configure(insertbackground="black")
        self.blueLevelText.configure(selectbackground="#c4c4c4")
        self.blueLevelText.configure(selectforeground="black")
        self.blueLevelText.configure(wrap="word")
        self.blueLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))

        self.ledSetButton = tk.Button(self.illuminatorFrame)
        self.ledSetButton.place(relx=0.062, rely=0.81, height=64, width=300
                , bordermode='ignore')
        self.ledSetButton.configure(activebackground="#ececec")
        self.ledSetButton.configure(activeforeground="#000000")
        self.ledSetButton.configure(background="#b7b7b7")
        self.ledSetButton.configure(disabledforeground="#a3a3a3")
        self.ledSetButton.configure(foreground="#000000")
        self.ledSetButton.configure(highlightbackground="#d9d9d9")
        self.ledSetButton.configure(highlightcolor="black")
        self.ledSetButton.configure(pady="0")
        self.ledSetButton.configure(text='''Set''')
        self.ledSetButton.configure(command= self.setLed)
        self.ledSetButton.configure(font=font20)


        self.redLevelLabel = tk.Label(self.illuminatorFrame)
        self.redLevelLabel.place(relx=0.4, rely=0.32, height=26, width=175
                , bordermode='ignore')
        self.redLevelLabel.configure(activebackground="#f9f9f9")
        self.redLevelLabel.configure(activeforeground="black")
        self.redLevelLabel.configure(background="#d9d9d9")
        self.redLevelLabel.configure(disabledforeground="#a3a3a3")
        self.redLevelLabel.configure(foreground="#000000")
        self.redLevelLabel.configure(highlightbackground="#d9d9d9")
        self.redLevelLabel.configure(highlightcolor="black")
        self.redLevelLabel.configure(text='''Red(0-255)''')
        self.redLevelLabel.configure(font=font20)

        self.greenLevelLabel = tk.Label(self.illuminatorFrame)
        self.greenLevelLabel.place(relx=0.41, rely=0.51, height=26, width=183
                , bordermode='ignore')
        self.greenLevelLabel.configure(activebackground="#f9f9f9")
        self.greenLevelLabel.configure(activeforeground="black")
        self.greenLevelLabel.configure(background="#d9d9d9")
        self.greenLevelLabel.configure(disabledforeground="#a3a3a3")
        self.greenLevelLabel.configure(foreground="#000000")
        self.greenLevelLabel.configure(highlightbackground="#d9d9d9")
        self.greenLevelLabel.configure(highlightcolor="black")
        self.greenLevelLabel.configure(text='''Green(0-255)''')
        self.greenLevelLabel.configure(font=font20)

        

        self.blueLevelLabel = tk.Label(self.illuminatorFrame)
        self.blueLevelLabel.place(relx=0.387, rely=0.698, height=26, width=180
                , bordermode='ignore')
        self.blueLevelLabel.configure(activebackground="#f9f9f9")
        self.blueLevelLabel.configure(activeforeground="black")
        self.blueLevelLabel.configure(background="#d9d9d9")
        self.blueLevelLabel.configure(disabledforeground="#a3a3a3")
        self.blueLevelLabel.configure(foreground="#000000")
        self.blueLevelLabel.configure(highlightbackground="#d9d9d9")
        self.blueLevelLabel.configure(highlightcolor="black")
        self.blueLevelLabel.configure(justify='left')
        self.blueLevelLabel.configure(text='''Blue(0-255)''')
        self.blueLevelLabel.configure(font=font20)


        self.carouselFrame = tk.LabelFrame(top)
        self.carouselFrame.place(relx=0.006, rely=0.64, relheight=0.3452
                , relwidth=0.192)
        self.carouselFrame.configure(relief='groove')
        self.carouselFrame.configure(borderwidth="8")
        self.carouselFrame.configure(font=font25)
        self.carouselFrame.configure(foreground="black")
        self.carouselFrame.configure(text='''Carousel''')
        self.carouselFrame.configure(background="#d9d9d9")
        self.carouselFrame.configure(highlightbackground="#d9d9d9")
        self.carouselFrame.configure(highlightcolor="black")

        self.minusStepCarouselButton = tk.Button(self.carouselFrame)
        self.minusStepCarouselButton.place(relx=0.062, rely=0.135, height=64, width=150
                , bordermode='ignore')
        self.minusStepCarouselButton.configure(activebackground="#ececec")
        self.minusStepCarouselButton.configure(activeforeground="#000000")
        self.minusStepCarouselButton.configure(background="#b7b7b7")
        self.minusStepCarouselButton.configure(disabledforeground="#a3a3a3")
        self.minusStepCarouselButton.configure(foreground="#000000")
        self.minusStepCarouselButton.configure(highlightbackground="#d9d9d9")
        self.minusStepCarouselButton.configure(highlightcolor="black")
        self.minusStepCarouselButton.configure(pady="0")
        self.minusStepCarouselButton.configure(text='''Step(-)''')
        self.minusStepCarouselButton.configure(command= self.cwStep)
        self.minusStepCarouselButton.configure(font=font20)

        self.plusStepCarouselButton = tk.Button(self.carouselFrame)
        self.plusStepCarouselButton.place(relx=0.497, rely=0.135, height=64, width=150
                , bordermode='ignore')
        self.plusStepCarouselButton.configure(activebackground="#ececec")
        self.plusStepCarouselButton.configure(activeforeground="#000000")
        self.plusStepCarouselButton.configure(background="#b7b7b7")
        self.plusStepCarouselButton.configure(disabledforeground="#a3a3a3")
        self.plusStepCarouselButton.configure(foreground="#000000")
        self.plusStepCarouselButton.configure(highlightbackground="#d9d9d9")
        self.plusStepCarouselButton.configure(highlightcolor="black")
        self.plusStepCarouselButton.configure(pady="0")
        self.plusStepCarouselButton.configure(text='''Step(+)''')
        self.plusStepCarouselButton.configure(command= self.ccwStep)
        self.plusStepCarouselButton.configure(font=font20)


        self.zeroCarouselButton = tk.Button(self.carouselFrame)
        self.zeroCarouselButton.place(relx=0.062, rely=0.439, height=64, width=300
                , bordermode='ignore')
        self.zeroCarouselButton.configure(activebackground="#ececec")
        self.zeroCarouselButton.configure(activeforeground="#ffffff")
        self.zeroCarouselButton.configure(background="#b7b7b7")
        self.zeroCarouselButton.configure(disabledforeground="#a3a3a3")
        self.zeroCarouselButton.configure(foreground="#000000")
        self.zeroCarouselButton.configure(highlightbackground="#d9d9d9")
        self.zeroCarouselButton.configure(highlightcolor="#ffffff")
        self.zeroCarouselButton.configure(pady="0")
        self.zeroCarouselButton.configure(text='''Zero''')
        self.zeroCarouselButton.configure(command= self.zeroCarousel)
        self.zeroCarouselButton.configure(font=font20)


        self.goToSlideText = tk.Text(self.carouselFrame)
        self.goToSlideText.place(relx=0.062, rely=0.709, relheight=0.203
                , relwidth=0.329, bordermode='ignore')
        self.goToSlideText.configure(background="white")
        self.goToSlideText.configure(font=font20)
        self.goToSlideText.configure(foreground="black")
        self.goToSlideText.configure(highlightbackground="#d9d9d9")
        self.goToSlideText.configure(highlightcolor="black")
        self.goToSlideText.configure(insertbackground="black")
        self.goToSlideText.configure(selectbackground="#c4c4c4")
        self.goToSlideText.configure(selectforeground="black")
        self.goToSlideText.configure(wrap="word")
        self.goToSlideText.bind("<Button-1>",lambda e: self.genKeyPad(e))


        self.goToSlideButton = tk.Button(self.carouselFrame)
        self.goToSlideButton.place(relx=0.435, rely=0.709, height=64, width=164
                , bordermode='ignore')
        self.goToSlideButton.configure(activebackground="#ececec")
        self.goToSlideButton.configure(activeforeground="#000000")
        self.goToSlideButton.configure(background="#b7b7b7")
        self.goToSlideButton.configure(disabledforeground="#a3a3a3")
        self.goToSlideButton.configure(foreground="#000000")
        self.goToSlideButton.configure(highlightbackground="#d9d9d9")
        self.goToSlideButton.configure(highlightcolor="black")
        self.goToSlideButton.configure(pady="0")
        self.goToSlideButton.configure(text='''Go to Slide''')
        self.goToSlideButton.configure(command= self.goToSlide)
        self.goToSlideButton.configure(font=font20)

        self.sampleParamsFrame = tk.LabelFrame(top)
        self.sampleParamsFrame.place(relx=0.787, rely=0.649, relheight=0.342
                , relwidth=0.208)
        self.sampleParamsFrame.configure(relief='groove')
        self.sampleParamsFrame.configure(borderwidth="8")
        self.sampleParamsFrame.configure(font=font25)
        self.sampleParamsFrame.configure(foreground="black")
        self.sampleParamsFrame.configure(text='''Sample Parameters''')
        self.sampleParamsFrame.configure(background="#d9d9d9")
        self.sampleParamsFrame.configure(highlightbackground="#d9d9d9")
        self.sampleParamsFrame.configure(highlightcolor="black")

        self.sampleIdText = tk.Text(self.sampleParamsFrame)
        self.sampleIdText.place(relx=0.062, rely=0.131, relheight=0.157
                , relwidth=0.335, bordermode='ignore')
        self.sampleIdText.configure(background="white")
        self.sampleIdText.configure(font=font20)
        self.sampleIdText.configure(foreground="black")
        self.sampleIdText.configure(highlightbackground="#d9d9d9")
        self.sampleIdText.configure(highlightcolor="black")
        self.sampleIdText.configure(insertbackground="black")
        self.sampleIdText.configure(selectbackground="#c4c4c4")
        self.sampleIdText.configure(selectforeground="black")
        self.sampleIdText.configure(wrap="word")

        self.sampleDateText = tk.Text(self.sampleParamsFrame)
        self.sampleDateText.place(relx=0.062, rely=0.327, relheight=0.157
                , relwidth=0.335, bordermode='ignore')
        self.sampleDateText.configure(background="white")
        self.sampleDateText.configure(font=font20)
        self.sampleDateText.configure(foreground="black")
        self.sampleDateText.configure(highlightbackground="#d9d9d9")
        self.sampleDateText.configure(highlightcolor="black")
        self.sampleDateText.configure(insertbackground="black")
        self.sampleDateText.configure(selectbackground="#c4c4c4")
        self.sampleDateText.configure(selectforeground="black")
        self.sampleDateText.configure(wrap="word")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y")
        temp= dt_string.split('/')
        if(temp[0][0]=='0'):
            temp[0] = temp[0][1:]
        temp[2] = temp[2][2:]
        print(temp)
        dt_string="{}/{}/{}".format(temp[0],temp[1],temp[2])
        self.sampleDateText.insert(END,dt_string)

        self.sampleRatioText = tk.Text(self.sampleParamsFrame)
        self.sampleRatioText.place(relx=0.062, rely=0.523, relheight=0.157
                , relwidth=0.335, bordermode='ignore')
        self.sampleRatioText.configure(background="white")
        self.sampleRatioText.configure(font=font20)
        self.sampleRatioText.configure(foreground="black")
        self.sampleRatioText.configure(highlightbackground="#d9d9d9")
        self.sampleRatioText.configure(highlightcolor="black")
        self.sampleRatioText.configure(insertbackground="black")
        self.sampleRatioText.configure(selectbackground="#c4c4c4")
        self.sampleRatioText.configure(selectforeground="black")
        self.sampleRatioText.configure(wrap="word")
        



        self.sampleIdLabel = tk.Label(self.sampleParamsFrame)
        self.sampleIdLabel.place(relx=0.45, rely=0.171, height=24, width=140
                , bordermode='ignore')
        self.sampleIdLabel.configure(activebackground="#f9f9f9")
        self.sampleIdLabel.configure(activeforeground="black")
        self.sampleIdLabel.configure(background="#d9d9d9")
        self.sampleIdLabel.configure(disabledforeground="#a3a3a3")
        self.sampleIdLabel.configure(foreground="#000000")
        self.sampleIdLabel.configure(highlightbackground="#d9d9d9")
        self.sampleIdLabel.configure(highlightcolor="black")
        self.sampleIdLabel.configure(text='''Sample ID''')
        self.sampleIdLabel.configure(font=font20)

        self.sampleDateLabel = tk.Label(self.sampleParamsFrame)
        self.sampleDateLabel.place(relx=0.4, rely=0.377, height=24, width=100
                , bordermode='ignore')
        self.sampleDateLabel.configure(activebackground="#f9f9f9")
        self.sampleDateLabel.configure(activeforeground="black")
        self.sampleDateLabel.configure(background="#d9d9d9")
        self.sampleDateLabel.configure(disabledforeground="#a3a3a3")
        self.sampleDateLabel.configure(foreground="#000000")
        self.sampleDateLabel.configure(highlightbackground="#d9d9d9")
        self.sampleDateLabel.configure(highlightcolor="black")
        self.sampleDateLabel.configure(text='''Date''')
        self.sampleDateLabel.configure(font=font20)

        self.sampleRatioLabel = tk.Label(self.sampleParamsFrame)
        self.sampleRatioLabel.place(relx=0.41555, rely=0.5689, height=24, width=170
                , bordermode='ignore')
        self.sampleRatioLabel.configure(activebackground="#f9f9f9")
        self.sampleRatioLabel.configure(activeforeground="black")
        self.sampleRatioLabel.configure(background="#d9d9d9")
        self.sampleRatioLabel.configure(disabledforeground="#a3a3a3")
        self.sampleRatioLabel.configure(foreground="#000000")
        self.sampleRatioLabel.configure(highlightbackground="#d9d9d9")
        self.sampleRatioLabel.configure(highlightcolor="black")
        self.sampleRatioLabel.configure(text='''WBC : RBC''')
        self.sampleRatioLabel.configure(font=font20)

        self.sampleBloodCountText = tk.Text(self.sampleParamsFrame)
        self.sampleBloodCountText.place(relx=0.062, rely=0.752, relheight=0.157
                , relwidth=0.335, bordermode='ignore')
        self.sampleBloodCountText.configure(background="white")
        self.sampleBloodCountText.configure(font=font20)
        self.sampleBloodCountText.configure(foreground="black")
        self.sampleBloodCountText.configure(highlightbackground="#d9d9d9")
        self.sampleBloodCountText.configure(highlightcolor="black")
        self.sampleBloodCountText.configure(insertbackground="black")
        self.sampleBloodCountText.configure(selectbackground="#c4c4c4")
        self.sampleBloodCountText.configure(selectforeground="black")
        self.sampleBloodCountText.configure(wrap="word")

        self.sampleBloodCountLabel = tk.Label(self.sampleParamsFrame)
        self.sampleBloodCountLabel.place(relx=0.43, rely=0.796, height=24, width=100
                , bordermode='ignore')
        self.sampleBloodCountLabel.configure(activebackground="#f9f9f9")
        self.sampleBloodCountLabel.configure(activeforeground="black")
        self.sampleBloodCountLabel.configure(background="#d9d9d9")
        self.sampleBloodCountLabel.configure(disabledforeground="#a3a3a3")
        self.sampleBloodCountLabel.configure(foreground="#000000")
        self.sampleBloodCountLabel.configure(highlightbackground="#d9d9d9")
        self.sampleBloodCountLabel.configure(highlightcolor="black")
        self.sampleBloodCountLabel.configure(text='''Counts''')
        self.sampleBloodCountLabel.configure(font=font20)
        
        self.imageFrame = tk.LabelFrame(top)
        self.imageFrame.place(relx=0.3969, rely=0.006, relheight=0.638
                , relwidth=0.600)
        self.imageFrame.configure(relief='groove')
        self.imageFrame.configure(borderwidth="0")
#         self.imageFrame.configure(font=font25)
        self.imageFrame.configure(foreground="black")
#         self.imageFrame.configure(text='''Slide Image''')
        self.imageFrame.configure(background="#d9d9d9")
        self.imageFrame.configure(highlightbackground="#d9d9d9")
        self.imageFrame.configure(highlightcolor="black")

        size = 1975.68,833.49
        self.path = "/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"
        img = Image.open(self.path)
        img.thumbnail(size, Image.ANTIALIAS)
        
        self.img = ImageTk.PhotoImage(Image.open("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
#         self.img = ImageTk.PhotoImage(img)
        self.panel = tk.Label(self.imageFrame,image=self.img)
        self.panel.pack()
        
        self.system = System(self)

        


if __name__ == '__main__':
    vp_start_gui()
    
    




