import tkinter as tk
from System import System
from PIL import ImageTk, Image
from KeyPad import KeyPad
import os
from Camera import Camera
from CamAdjustFrame import CamAdjustFrame
from multiprocessing import Queue
from queue import Empty
from threading import Thread



class GUI:
     
    def __init__(self):
        
        #used to set memory requirement for Camera 
        os.system("sudo echo 0|sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb")

        '''This class configures and populates the toplevel window.
           self.root is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font25 = "-family {Segoe UI} -size 25 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font20 = "-family {Segoe UI} -size 20 -slant roman "  \
            "-underline 0 -overstrike 0"
        
        self.system = System(self) #system object that stores all objects for al functionality (gets passed the GUI)
        
        self.queue = Queue()#queue used for processing instructions from threads for updating GUI etc.
        
        #carousel zeroed flag and counters and keypad flag 
        self.carouselZeroed = False
        self.kpRunning = 0
        
        #counters to track whether button click opens or closes camera adjust window and on or off LED
        self.camAdjustCnt=0
        self.ledPowerCnt = 0
        
        
        
        
        #top-level configuration(window position, Title, Background color)
        self.root = tk.Tk()
        self.root.geometry("1920x1060+-1+-2")
        self.root.title("Blood Analyzer")
        self.root.configure(background="#d9d9d9")
        
        
        #configuration for health/ status frame which contains status (busy or ready) and camera temp (celsius)
        self.healthStatusFrame = tk.LabelFrame(self.root)
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
        self.statusText.insert(tk.END,"Ready")
        self.statusText.configure(highlightbackground="green")
        self.statusText.configure(highlightthickness=6)

        self.camTempText = tk.Text(self.healthStatusFrame)
        self.camTempText.place(relx=0.064, rely=0.61, relheight=0.282
                , relwidth=0.3, bordermode='ignore')
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
        self.camTempLabel.place(relx=0.39, rely=0.688, height=26, width=210
                , bordermode='ignore')
        self.camTempLabel.configure(font=font20)

        self.camTempLabel.configure(background="#d9d9d9")
        self.camTempLabel.configure(disabledforeground="#a3a3a3")
        self.camTempLabel.configure(foreground="#000000")
        self.camTempLabel.configure(text='''Cam Temp (°C)''')

        #configuration for the camera Frame which contains camera adjust button
        self.cameraFrame = tk.LabelFrame(self.root)
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
        self.camAdjustButton.configure(command = self.camAdjust) #callback for adjust button is self.camAdjust()


        #configuration for the Focus Frame which contains manual focus (+) (-) buttons, display for curPos, video button
        # and auto focus button 
        self.focusFrame = tk.LabelFrame(self.root)
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
        self.minusStepFocusButton.configure(command= self.jogDwn)#callback for manual step(-) is self.jogDwn()
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
        self.plusStepFocusButton.configure(command= self.jogUp)#callback for manual step(+) is self.jogUp()
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
        self.focusPosText.insert(tk.END,"10000")

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
        
        self.videoButton.configure(command=self.videoPower)#callback for video button is self.videoPower()

 
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
        self.autoFocusButton.configure(command = self.autoFocus) #threaded and hooked to e-stop
        self.autoFocusButton.configure(font=font20)

        #configuration for manual frame which contains capture image button, analyze sample button, and save data button
        self.manualFrame = tk.LabelFrame(self.root)
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
        self.captureImageButton.configure(command=self.showIm)#callback for capture image button is self.showIm()



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
        self.analyzeSampleButton.configure(command= self.countBlood)#callback for Analyze sample button is self.countBlood()
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
        self.saveDataButton.configure(command = self.saveData)#callback for Save data button is self.saveData()
        self.saveDataButton.configure(font=font20)


        #configuration for utility frame which contains create file button, open file button, and set pathology interface
        self.utilityFrame = tk.LabelFrame(self.root)
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
        self.createFileButton.configure(command= self.createFile)#callback for create file button is self.createFile()
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
        self.openFileButton.configure(command = self.openFile)#callback for open file button is self.openFile()
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
        self.setPathologyButton.configure(command = self.setPathology)#callback for set pathology button is self.setPathology()
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
        self.minPathologyText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for min patholgy text is self.genKeyPad(e)
        

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
        self.maxPathologyText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for max patholgy text is self.genKeyPad(e)

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


        #configuration for automatic frame which contains auto-start button and E-stop button
        self.automaticFrame = tk.LabelFrame(self.root)
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
        self.autoStartButton.configure(command= self.autoStart)#callback for auto start buttton is self.autoStart()
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
        self.emergencyStopButton.configure(command= self.eStop)#callback for e-stop buttton is self.eStop()


        #configuration for illuminator frame which contains input text boxes for RGB values, on/off button, and set button 
        self.illuminatorFrame = tk.LabelFrame(self.root)
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
        self.ledPowerButton.configure(text='''On/Off''')
        self.ledPowerButton.configure(command= self.ledPower)#callback for led power buttton is self.ledPower()
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
        self.redLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for red level text is self.genKeyPad(e)

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
        self.greenLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for green level text is self.genKeyPad(e)

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
        self.blueLevelText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for blue level text is self.genKeyPad(e)

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
        self.ledSetButton.configure(command= self.setLed)#callback for set led buttton is self.setLed()
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

        #configuration for carousel frame which contains manual step forward and backward buttons,
        #zero carousel button, and go to slide interface
        self.carouselFrame = tk.LabelFrame(self.root)
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
        self.minusStepCarouselButton.configure(command= self.cwStep)#callback for single step minus is self.cwStep()
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
        self.plusStepCarouselButton.configure(command= self.ccwStep)#callback for single step plus is self.ccwStep()
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
        self.zeroCarouselButton.configure(command= self.zeroCarousel)#callback for zero carousel button is self.zeroCarousel()
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
        self.goToSlideText.bind("<Button-1>",lambda e: self.genKeyPad(e))#callback for go to slide text is self.genKeyPad(e)


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
        self.goToSlideButton.configure(command= self.goToSlide)#callback for go to slide button is self.goToSlide()
        self.goToSlideButton.configure(font=font20)


        #configuration for sample parameters frame which contains sample id, sample data, wbc/rbc ratio and wbc/rbc counts 
        self.sampleParamsFrame = tk.LabelFrame(self.root)
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
        
        #configuration for image frame that contains the current image
        self.imageFrame = tk.LabelFrame(self.root)
        self.imageFrame.place(relx=0.3969, rely=0.006, relheight=0.638
                , relwidth=0.600)
        self.imageFrame.configure(relief='groove')
        self.imageFrame.configure(borderwidth="0")
        self.imageFrame.configure(foreground="black")
        self.imageFrame.configure(background="#d9d9d9")
        self.imageFrame.configure(highlightbackground="#d9d9d9")
        self.imageFrame.configure(highlightcolor="black")

        self.path = "xi_example.tiff"

        
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel = tk.Label(self.imageFrame,image=self.img)
        self.panel.image = self.img
        self.panel.pack()
        
        
        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%~~~~~~~~~~BEGIN CALLBACKS~~~~~~~~~~~~%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# 1.)  CAMERA                                                                                                             #
# 2.)  FOCUS                                                                                                              #
# 3.)  ANALYZE BLOOD                                                                                                      #
# 4.)  BORDER UPDATE                                                                                                      #
# 5.)  DATAFILE                                                                                                           #
# 6.)  AUTO START & E-STOP                                                                                                #
# 7.)  LED                                                                                                                #
# 8.)  CAROUSEL                                                                                                           #
# 9.)  KEYPAD                                                                                                             #
# 10.) RUN                                                                                                                #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#


        
        


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CAMERA FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #opens and closes cam adjust window based on parity of counter
    def camAdjust(self):
        if(self.camAdjustCnt %2 == 0):
            self.system.cam.camAdjust()
        else:
            self.system.cam.camAdjustExit()
        self.camAdjustCnt+=1
        
    #updates Cam Temp Reading every 6 secs   
    def getCamTemp(self):
        x = self.system.cam.getTemp()
        x =str(round(x,2))
        self.camTempText.delete("1.0","end")
        self.camTempText.insert(tk.END,x)
        self.root.after(6000,self.getCamTemp)
    
    #shows Image on GUI after capture image is pressed
    def showIm(self):
        
        self.updateStatusText("Camera Busy")
        self.updateStatusBorder("yellow")
        self.system.busy = True
        self.system.cam.showIm()
        self.system.busy = False
        self.system.GUI.updateStatusText()
        self.system.GUI.updateStatusBorder()
     
    #prints camera aq status every 6 seconds (useful for debugging) 
    def camAqStatus(self):
        print(self.system.cam.getAqStatus())
        self.root.after(6000,self.camAqStatus)
        
    #every 100ms checks if image needs to be updated and updates when necessary    
    def updateImage(self):
        if(self.system.imgChange==True):
            self.newImg = ImageTk.PhotoImage(self.system.currImage)
            self.panel.configure(image=self.newImg)
            self.panel.image = self.newImg
            self.panel.pack()
            self.system.imgChange = False
        self.root.after(100,self.updateImage)
        
    #starts new seperate thread for video calling system.control, which is for controlling threads
    #thread runs in a infinite loop, checking parity of vidPowerCnt to determine when to turn on or off
    #can be killed by e-stop(thread not killed,but video turned off)
    def videoPower(self):
        if(self.system.cam.vidPowerCnt %2 == 0):
            
            self.updateStatusText("Camera Busy")
            self.updateStatusBorder("yellow")
            self.system.busy = True
            if(self.system.videoThreadStarted==False):
                
                self.system.control.combine('cam')

        else:
            self.system.busy = False
            self.system.GUI.updateStatusText()
            self.system.GUI.updateStatusBorder()
        self.system.cam.vidPowerCnt +=1



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FOCUS FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


    #runs autofoucs routine in seperate thread, can be killed by e-stop
    def autoFocus(self):
        self.system.control.combine('focus')
        

    #manual single step down   
    def jogDwn(self):
        self.system.focus.jogDown()
        self.focusPosText.delete("1.0", "end")
        self.focusPosText.insert(tk.END,self.system.focus.zVar())
    
    #manual single step up 
    def jogUp(self):
        self.system.focus.jogUp()
        self.focusPosText.delete("1.0", "end")
        self.focusPosText.insert(tk.END,self.system.focus.zVar())
        



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ANALYZE BLOOD FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
        
    #runs blood counting in seperate thread, cannot be killed by e-stop (but could easily be added)
    def countBlood(self):
        self.updateStatusText("Analyzing Blood")
        self.updateStatusBorder("yellow")
        self.system.busy = True
        analyze = Thread(target = self.system.man.countBlood)
        analyze.start()
        

    #sets pathology in utility class from user input into min and max pathology 
    def setPathology(self):
        self.system.util.setPathology(float(self.minPathologyText.get("1.0",tk.END)),float(self.maxPathologyText.get("1.0",tk.END)))
 
 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BORDER UPDATE FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
 
 
    #added next two functions to remove/add pathology border. root.update()
    #forces the GUI to redraw (fixed issue of not remoiving border at new analysis)
    #root.update is dangerous and i'm not sure if its causing nested event loops
    # should probably switch to root.after similar to camTemp function 
    def removePathologyBorder(self):
        self.sampleBloodCountText.delete("1.0", "end")
        self.sampleRatioText.delete("1.0", "end")
        self.sampleRatioText.configure(highlightthickness=0)
        self.root.update()
        
    #for setting red border on wbc/rbc ratio on GUI, same warning as above 
    def addPathologyBorder(self,ratio):
        if(self.system.util.pathologyWarn(ratio)):
            self.sampleRatioText.configure(highlightbackground="red")
            self.sampleRatioText.configure(highlightthickness=6)
            self.root.update()
            
   #for setting status border on GUI, same warning as above 
    def updateStatusBorder(self,color="green"):
        if(self.system.busy == True):
            return
        self.statusText.configure(highlightbackground=color)
        self.statusText.configure(highlightthickness=6)
        self.root.update()
        
    def updateStatusText(self,display_text="Ready"):
        if(self.system.busy == True):
            return
        
        self.statusText.delete("1.0", "end")
        self.statusText.insert(tk.END,display_text)
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA FILE FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#        
            
            
    #saves data from analysis, should be used right after analyze sample is pressed 
    def saveData(self):
        self.system.man.saveData()
    
    #creates a dataFile
    def createFile(self):
        self.system.util.createFile()
        
    #opens dataFile in Libre office
    def openFile(self):
        self.system.util.openCurrFile()
  

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AUTO START & E-STOP FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #start automatic mode in separate thread, can be killed by e-stop
    def autoStart(self):
        self.sampleBloodCountText.delete("1.0", "end")
        self.sampleRatioText.delete("1.0", "end")
        self.removePathologyBorder()
        self.system.control.combine('auto')
        
        
    #kills threads, except video thread(in that case it just calls videoPower
    def eStop(self):
        cam =False
        if(self.system.cam.vidPowerCnt %2 == 1):
            cam = True
        self.system.control.stop(cam)
        
        
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
# should add a setBrightness function and modify GUI to support that function (lighting is very important for camera)    #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #turns led on and off based on parity of number of clicks (for some reason the first power on, it must be turned on, off, on to get it on)  
    def ledPower(self):
        if(self.ledPowerCnt % 2 == 0):
            self.system.illuminator.turnOn()
            if(self.ledPowerCnt==0):
                self.system.illuminator.turnOff()
                self.system.illuminator.turnOn()
        else:
            self.system.illuminator.turnOff()
        self.ledPowerCnt +=1
    
    #changes LED color based on values input by user 
    def setLed(self):
        self.system.illuminator.changeColor(int(self.redLevelText.get("1.0",tk.END)),int(self.greenLevelText.get("1.0",tk.END)),int(self.blueLevelText.get("1.0",tk.END)))



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CAROUSEL FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #single step ccw
    def ccwStep(self):
        self.system.carousel.stepForward()
    
    #single step cw
    def cwStep(self):
        self.system.carousel.stepBackward()
    
    #zero carousel and show 0 for slide position, display sample date and ID in sample params frame if present in the datafile
    def zeroCarousel(self):
        self.system.carousel.zeroPos()
        self.carouselZeroed = True
        self.goToSlideText.delete("1.0","end")
        self.goToSlideText.insert(tk.END, '0')
        try:
            self.sampleIdText.delete("1.0","end")
            self.sampleDateText.delete("1.0","end")
            self.sampleIdText.insert(tk.END,self.system.fileHandler.readSampleID())
            self.sampleDateText.insert(tk.END,self.system.fileHandler.readSampleDate())
            
        except:
            print("Error: could not insert sampleID or sampleDate to GUI")
    
    
    #go to specified slide, update carousel position displayed on GUI, remove patholgy border if present, and display sample ID
    #and Date if present in the datafile 
    def goToSlide(self):
        self.sampleBloodCountText.delete("1.0", "end")
        self.sampleRatioText.delete("1.0", "end")
        self.removePathologyBorder()
        self.system.carousel.moveToSlide(int(self.goToSlideText.get("1.0",tk.END)))
        
        
        print("the carousel curPos is {}".format(self.system.carousel.curPos))
        try:
            self.sampleIdText.delete("1.0","end")
            self.sampleDateText.delete("1.0","end")
            self.sampleIdText.insert(tk.END,self.system.fileHandler.readSampleID())
            self.sampleDateText.insert(tk.END,self.system.fileHandler.readSampleDate())
        except:
            print("Error: could not insert sampleID or sampleDate to GUI")
            
            
            
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ KEYPAD FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #generates a keypad for user input knows which widget it was called from
    def genKeyPad(self,event):
        if(self.kpRunning==0):
            r = tk.Tk()
            r.call('wm', 'attributes', '.', '-topmost', '1') #keeps the keypad on top
            caller = event.widget
#             print(caller)
            r.title("Keypad")
            r.overrideredirect(True) #disallows user exiting keypad with x button 

            kp = KeyPad(r,self,caller)
            kp.grid()
            
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUN FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    def run(self):
        self.getCamTemp() #updates cam temp every 6 seconds
        self.process_queue()#process Thread queue
        self.updateImage()#updates current image displayed on GUI when necessary
#         self.camAqStatus()
        self.root.mainloop()
        
    #checks queue for data from different threads every 100 ms   
    def process_queue(self):
        if(not self.queue.empty()):
            msg = self.queue.get(0)#get method returns and removes item. This is a FIFO queue
#             print("what main loop sees in q :",msg)
            
            #message to set status to Ready
            if(msg == 'setReady'):
                self.system.busy = False
                self.system.GUI.updateStatusText()
                self.system.GUI.updateStatusBorder()
             
            #updates sample params and current slide position, as well as adds pathology border
            #these data come from blood analysis thread or automatic thread
            if(isinstance(msg,list)):
                if(msg[0]== 'countblood'):
                    self.system.busy = False
                    self.system.GUI.updateStatusText()
                    self.system.GUI.updateStatusBorder()
                    
#                 print("whole thing: ",msg)
#                 print("~~~~~~~~~~~~~PARTS~~~~~~~")
#                 print(msg[0])
#                 print(msg[1])
#                 print(msg[2])
#                 print(msg[3])
#                 print(msg[4])
#                 print(msg[5])
                    
                self.sampleBloodCountText.delete("1.0", "end")
                self.sampleBloodCountText.insert(tk.END,"{}/{}".format(msg[1],msg[2]))
                self.sampleRatioText.delete("1.0", "end")    
                self.sampleRatioText.insert(tk.END,"{}".format(msg[3]))
                self.sampleIdText.delete("1.0", "end")
                self.goToSlideText.delete("1.0","end")
                self.goToSlideText.insert(tk.END,msg[5])
                self.addPathologyBorder(msg[3])
                
            #mesage to remove pathology border    
            if(msg == 'removePathBorder'):
                print("removed path border")
                self.removePathologyBorder()
                
                    
        self.root.after(100, self.process_queue)# run inifinite loop (recursion)

#start GUI
app = GUI()
app.run()

        


        



    
    






