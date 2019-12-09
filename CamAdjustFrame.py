from tkinter import *

#this class creates the camera adjust frame 

class CamAdjustFrame(Frame):
    """ GUI frame for camera adjust interface """

    def __init__(self, master,system):
        
        """ initialize the frame """
        
        self.system = system
        self.master = master
        self.kr = '{:5.2f}'.format(self.system.cam.get_kr())
        self.kg = '{:5.2f}'.format(self.system.cam.get_kg())
        self.kb = '{:5.2f}'.format(self.system.cam.get_kb())
        self.exp = self.system.cam.get_exp()
        self.sharp = '{:5.1f}'.format(self.system.cam.get_sharp())
        super(CamAdjustFrame, self).__init__(master)
        self.configure(background ="blue")
        self.pack()
#         self.autoWBCnt = 0    
        self.FONT = "-family {Segoe UI} -size 25 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        self.font20 = "-family {Segoe UI} -size 20 -slant roman "  \
            "-underline 0 -overstrike 0"
        self.create_buttons()
        
        
            

    def create_buttons(self):
        self.wbFrame = LabelFrame(self, width = 400, height =450)
        self.wbFrame.configure(relief='groove')
        self.wbFrame.configure(borderwidth="8")
        self.wbFrame.configure(font=self.FONT)
        self.wbFrame.configure(foreground="black")
        self.wbFrame.configure(text='''White Balance''')
        self.wbFrame.configure(background="#d9d9d9")
        self.wbFrame.configure(highlightbackground="#d9d9d9")
        self.wbFrame.configure(highlightcolor="black")
        self.wbFrame.pack()

        self.wbAutoButton = Button(self.wbFrame)
        self.wbAutoButton.place(relx=0.062, rely=0.093, height=64, width=300
                , bordermode='ignore')
  
        self.wbAutoButton.configure(activebackground="#757575")
        self.wbAutoButton.configure(activeforeground="white")
        self.wbAutoButton.configure(activeforeground="#000000")
        self.wbAutoButton.configure(background="#b7b7b7")
        self.wbAutoButton.configure(disabledforeground="#a3a3a3")
        self.wbAutoButton.configure(foreground="#000000")
        self.wbAutoButton.configure(highlightbackground="#d9d9d9")
        self.wbAutoButton.configure(highlightcolor="black")
        self.wbAutoButton.configure(pady="0")
        if(self.system.cam.is_auto_wb()):
            t = '''Auto Off'''
        else:
            t = '''Auto On'''
        self.wbAutoButton.configure(text=t)
        self.wbAutoButton.configure(command= self.toggleAutoWB)
        self.wbAutoButton.configure(font=self.font20)


        self.redLevelText = Text(self.wbFrame)
        self.redLevelText.place(relx=0.062, rely=0.278, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.redLevelText.configure(background="white")
        self.redLevelText.configure(font=self.font20)
        self.redLevelText.configure(foreground="black")
        self.redLevelText.configure(highlightbackground="#d9d9d9")
        self.redLevelText.configure(highlightcolor="black")
        self.redLevelText.configure(insertbackground="black")
        self.redLevelText.configure(selectbackground="#c4c4c4")
        self.redLevelText.configure(selectforeground="black")
        self.redLevelText.configure(wrap="word")
        self.redLevelText.bind("<Button-1>",lambda e: self.system.GUI.genKeyPad(e))
        self.redLevelText.insert(END,self.kr)

        self.greenLevelText = Text(self.wbFrame)
        self.greenLevelText.place(relx=0.062, rely=0.463, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.greenLevelText.configure(background="white")
        self.greenLevelText.configure(font=self.font20)
        self.greenLevelText.configure(foreground="black")
        self.greenLevelText.configure(highlightbackground="#d9d9d9")
        self.greenLevelText.configure(highlightcolor="black")
        self.greenLevelText.configure(insertbackground="black")
        self.greenLevelText.configure(selectbackground="#c4c4c4")
        self.greenLevelText.configure(selectforeground="black")
        self.greenLevelText.configure(wrap="word")
        self.greenLevelText.bind("<Button-1>",lambda e: self.system.GUI.genKeyPad(e))
        self.greenLevelText.insert(END,self.kg)

        self.blueLevelText = Text(self.wbFrame)
        self.blueLevelText.place(relx=0.062, rely=0.648, relheight=0.139
                , relwidth=0.329, bordermode='ignore')
        self.blueLevelText.configure(background="white")
        self.blueLevelText.configure(font=self.font20)
        self.blueLevelText.configure(foreground="black")
        self.blueLevelText.configure(highlightbackground="#d9d9d9")
        self.blueLevelText.configure(highlightcolor="black")
        self.blueLevelText.configure(insertbackground="black")
        self.blueLevelText.configure(selectbackground="#c4c4c4")
        self.blueLevelText.configure(selectforeground="black")
        self.blueLevelText.configure(wrap="word")
        self.blueLevelText.bind("<Button-1>",lambda e: self.system.GUI.genKeyPad(e))
        self.blueLevelText.insert(END,self.kb)
        

        self.wbSetButton = Button(self.wbFrame)
        self.wbSetButton.place(relx=0.062, rely=0.81, height=64, width=300
                , bordermode='ignore')
        self.wbSetButton.configure(activebackground="#ececec")
        self.wbSetButton.configure(activeforeground="#000000")
        self.wbSetButton.configure(background="#b7b7b7")
        self.wbSetButton.configure(disabledforeground="#a3a3a3")
        self.wbSetButton.configure(foreground="#000000")
        self.wbSetButton.configure(highlightbackground="#d9d9d9")
        self.wbSetButton.configure(highlightcolor="black")
        self.wbSetButton.configure(pady="0")
        self.wbSetButton.configure(text='''Manual Set''')
        self.wbSetButton.configure(command= self.setManualWBalance)
        self.wbSetButton.configure(font=self.font20)


        self.redLevelLabel = Label(self.wbFrame)
        self.redLevelLabel.place(relx=0.4, rely=0.32, height=26, width=175
                , bordermode='ignore')
        self.redLevelLabel.configure(activebackground="#f9f9f9")
        self.redLevelLabel.configure(activeforeground="black")
        self.redLevelLabel.configure(background="#d9d9d9")
        self.redLevelLabel.configure(disabledforeground="#a3a3a3")
        self.redLevelLabel.configure(foreground="#000000")
        self.redLevelLabel.configure(highlightbackground="#d9d9d9")
        self.redLevelLabel.configure(highlightcolor="black")
        self.redLevelLabel.configure(text='''red(0-10)''')
        self.redLevelLabel.configure(font=self.font20)

        self.greenLevelLabel = Label(self.wbFrame)
        self.greenLevelLabel.place(relx=0.41, rely=0.51, height=26, width=183
                , bordermode='ignore')
        self.greenLevelLabel.configure(activebackground="#f9f9f9")
        self.greenLevelLabel.configure(activeforeground="black")
        self.greenLevelLabel.configure(background="#d9d9d9")
        self.greenLevelLabel.configure(disabledforeground="#a3a3a3")
        self.greenLevelLabel.configure(foreground="#000000")
        self.greenLevelLabel.configure(highlightbackground="#d9d9d9")
        self.greenLevelLabel.configure(highlightcolor="black")
        self.greenLevelLabel.configure(text='''green(0-10)''')
        self.greenLevelLabel.configure(font=self.font20)

        

        self.blueLevelLabel = Label(self.wbFrame)
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
        self.blueLevelLabel.configure(text='''blue(0-10)''')
        self.blueLevelLabel.configure(font=self.font20)
        
        
        
        
        self.exposureFrame = LabelFrame(self, width = 400, height =288)
        self.exposureFrame.place(relx=0.169, rely=0.159, relheight=0.483
                , relwidth=0.192)
        self.exposureFrame.configure(relief='groove')
        self.exposureFrame.configure(borderwidth="8")
        self.exposureFrame.configure(font=self.FONT)
        self.exposureFrame.configure(foreground="black")
        self.exposureFrame.configure(text='''Exposure''')
        self.exposureFrame.configure(background="#d9d9d9")
        self.exposureFrame.configure(highlightbackground="#d9d9d9")
        self.exposureFrame.configure(highlightcolor="black")
        self.exposureFrame.pack()
        
        
        self.AutoExposureButton = Button(self.exposureFrame)
        self.AutoExposureButton.place(relx=0.062, y=42, height=64, width=300
                , bordermode='ignore')
        self.AutoExposureButton.configure(activebackground="#ececec")
        self.AutoExposureButton.configure(activeforeground="#000000")
        self.AutoExposureButton.configure(background="#b7b7b7")
        self.AutoExposureButton.configure(disabledforeground="#a3a3a3")
        self.AutoExposureButton.configure(foreground="#000000")
        self.AutoExposureButton.configure(highlightbackground="#d9d9d9")
        self.AutoExposureButton.configure(highlightcolor="black")
        self.AutoExposureButton.configure(pady="0")
        if(self.system.cam.is_ag()):
            te = '''Auto Off'''
        else:
            te = '''Auto On'''
        self.AutoExposureButton.configure(text=te)
        self.AutoExposureButton.configure(command= self.toggle_ag)
        self.AutoExposureButton.configure(font=self.font20)
        
        
        
        self.exposureLabel = Label(self.exposureFrame)
        self.exposureLabel.place(relx=0.387, y= 144, height=26, width=175
                , bordermode='ignore')
        self.exposureLabel.configure(activebackground="#f9f9f9")
        self.exposureLabel.configure(activeforeground="black")
        self.exposureLabel.configure(background="#d9d9d9")
        self.exposureLabel.configure(disabledforeground="#a3a3a3")
        self.exposureLabel.configure(foreground="#000000")
        self.exposureLabel.configure(highlightbackground="#d9d9d9")
        self.exposureLabel.configure(highlightcolor="black")
        self.exposureLabel.configure(text='''(micro sec)''')
        self.exposureLabel.configure(font=self.font20)
        
        self.exposureText = Text(self.exposureFrame)
        self.exposureText.place(relx=0.062, y=122, height=64
                , relwidth=0.329, bordermode='ignore')
        self.exposureText.configure(background="white")
        self.exposureText.configure(font=self.font20)
        self.exposureText.configure(foreground="black")
        self.exposureText.configure(highlightbackground="#d9d9d9")
        self.exposureText.configure(highlightcolor="black")
        self.exposureText.configure(insertbackground="black")
        self.exposureText.configure(selectbackground="#c4c4c4")
        self.exposureText.configure(selectforeground="black")
        self.exposureText.configure(wrap="word")
        self.exposureText.bind("<Button-1>",lambda e: self.system.GUI.genKeyPad(e))
        self.exposureText.insert(END,self.exp)
        
        self.exposureSetButton = Button(self.exposureFrame)
        self.exposureSetButton.place(relx=0.062, y=202, height=64, width=300
                , bordermode='ignore')
        self.exposureSetButton.configure(activebackground="#ececec")
        self.exposureSetButton.configure(activeforeground="#000000")
        self.exposureSetButton.configure(background="#b7b7b7")
        self.exposureSetButton.configure(disabledforeground="#a3a3a3")
        self.exposureSetButton.configure(foreground="#000000")
        self.exposureSetButton.configure(highlightbackground="#d9d9d9")
        self.exposureSetButton.configure(highlightcolor="black")
        self.exposureSetButton.configure(pady="0")
        self.exposureSetButton.configure(text='''Manual Set''')
        self.exposureSetButton.configure(command= self.setExposure)
        self.exposureSetButton.configure(font=self.font20)
        
        
        
        self.sharpFrame = LabelFrame(self, width = 400, height =200)
        self.sharpFrame.place(relx=0.169, rely=0.159, relheight=0.483
                , relwidth=0.192)
        self.sharpFrame.configure(relief='groove')
        self.sharpFrame.configure(borderwidth="8")
        self.sharpFrame.configure(font=self.FONT)
        self.sharpFrame.configure(foreground="black")
        self.sharpFrame.configure(text='''Sharpness''')
        self.sharpFrame.configure(background="#d9d9d9")
        self.sharpFrame.configure(highlightbackground="#d9d9d9")
        self.sharpFrame.configure(highlightcolor="black")
        self.sharpFrame.pack()
        
        
        
        
        
        
        self.sharpLabel = Label(self.sharpFrame)
        self.sharpLabel.place(relx=0.387, y= 60, height=26, width=175
                , bordermode='ignore')
        self.sharpLabel.configure(activebackground="#f9f9f9")
        self.sharpLabel.configure(activeforeground="black")
        self.sharpLabel.configure(background="#d9d9d9")
        self.sharpLabel.configure(disabledforeground="#a3a3a3")
        self.sharpLabel.configure(foreground="#000000")
        self.sharpLabel.configure(highlightbackground="#d9d9d9")
        self.sharpLabel.configure(highlightcolor="black")
        self.sharpLabel.configure(text='''(0 to 8.0)''')
        self.sharpLabel.configure(font=self.font20)
        
        self.sharpText = Text(self.sharpFrame)
        self.sharpText.place(relx=0.062, y=40, height=64
                , relwidth=0.329, bordermode='ignore')
        self.sharpText.configure(background="white")
        self.sharpText.configure(font=self.font20)
        self.sharpText.configure(foreground="black")
        self.sharpText.configure(highlightbackground="#d9d9d9")
        self.sharpText.configure(highlightcolor="black")
        self.sharpText.configure(insertbackground="black")
        self.sharpText.configure(selectbackground="#c4c4c4")
        self.sharpText.configure(selectforeground="black")
        self.sharpText.configure(wrap="word")
        self.sharpText.bind("<Button-1>",lambda e: self.system.GUI.genKeyPad(e))
        self.sharpText.insert(END,self.sharp)
        
        self.sharpSetButton = Button(self.sharpFrame)
        self.sharpSetButton.place(relx=0.062, y=120, height=64, width=300
                , bordermode='ignore')
        self.sharpSetButton.configure(activebackground="#ececec")
        self.sharpSetButton.configure(activeforeground="#000000")
        self.sharpSetButton.configure(background="#b7b7b7")
        self.sharpSetButton.configure(disabledforeground="#a3a3a3")
        self.sharpSetButton.configure(foreground="#000000")
        self.sharpSetButton.configure(highlightbackground="#d9d9d9")
        self.sharpSetButton.configure(highlightcolor="black")
        self.sharpSetButton.configure(pady="0")
        self.sharpSetButton.configure(text='''Set''')
        self.sharpSetButton.configure(command= self.setSharp)
        self.sharpSetButton.configure(font=self.font20)


        
        
        
       
        
    #sets exposure value from user input
    def setExposure(self):
        if(self.system.cam.is_ag()):
            self.exposureSetButton.configure(text='''Auto On''')
            self.cam.diable_ag()
            
        data = int(self.exposureText.get("1.0",END))
        self.system.cam.cam.set_exposure(data)

    def setSharp(self):
        data = float(self.sharpText.get("1.0",END))
        data = data - 4
        print(type(data))
        print("val of sharp is",data)
        self.system.cam.setSharp(data)
    
    #turns auto white balance on and off based on parity of number of clicks 
    def toggleAutoWB(self):
        x = self.system.cam.is_auto_wb()
        if(x):
            self.disableAutoWBalance()
            self.wbAutoButton.config(text = '''Auto On''')
        
            
        else:
            self.enableAutoWBalance()
            self.wbAutoButton.config(text = '''Auto Off''')
            
        
    def toggle_ag(self):
        self.system.cam.toggle_ag()
    
    def enableAutoWBalance(self):
        self.system.cam.enableAutoWB()
        
    def disableAutoWBalance(self):
        self.system.cam.disableAutoWB()
        self.system.cam.stopAq()
        
    def updateVals(self):
        self.redLevelText.delete("1.0", "end")
        self.greenLevelText.delete("1.0", "end")
        self.blueLevelText.delete("1.0", "end")
        self.exposureText.delete("1.0", "end")
        self.sharpText.delete("1.0", "end")
        r = self.system.cam.get_kr()
        g = self.system.cam.get_kg()
        b = self.system.cam.get_kb()
        sharp = self.system.cam.get_sharp()
        exp = self.system.cam.get_exp()
        self.redLevelText.insert(END,r)
        self.greenLevelText.insert(END,g)
        self.blueLevelText.insert(END,b)
        self.exposureText.insert(END,exp)
        self.sharpText.insert(END,sharp)
        
        
        
        
       
    def setManualWBalance(self):
        if(self.system.cam.is_auto_wb()):
            self.wbAutoButton.config(text = '''Auto On''')
            self.disableAutoWBalance()
        self.system.cam.setManWB(float(self.redLevelText.get("1.0",END)),float(self.greenLevelText.get("1.0",END)),float(self.blueLevelText.get("1.0",END)))
        
       
    def cafExit(self):
        self.destroy()
        self.quit()
        self.master.destroy()
        self.master.quit()
       
       




