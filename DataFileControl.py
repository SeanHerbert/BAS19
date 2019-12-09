

from tkinter import *
import os
import subprocess
import signal



class DataFileControl(Frame):
    """ GUI frame with a text box and keypad """

    def __init__(self, master,system):
        
        """ initialize the frame """
        
        #stores current datafile name
        self.fname = system.dataFilePaths[system.currFileIndex][23:]
        self.master = master
        super(DataFileControl, self).__init__(master)
        self.grid()
            
        self.FONT = ("times bold", "20")
        self.create_buttons()
        self.proc1 = subprocess.Popen("florence",shell=True,preexec_fn=os.setsid)
            

    def create_buttons(self):

        # Create row 1 buttons
        self.btn_save = Button(self, text="Save", font=self.FONT,
                                command=self.save)
        self.btn_save.grid(row=1, column=0, sticky=W + E)
        self.btn_save.configure(width = 10)
        self.btn_save.configure(height = 2)


        self.btn_close = Button(self, text="Close", font=self.FONT,
                                command=self.close)
        self.btn_close.grid(row=1, column=1, sticky=W + E)
        self.btn_close.configure(width = 10)
        self.btn_close.configure(height = 2)
        
        
        #create row 2 buttons
        self.btn_scrollUp = Button(self, text = "Scroll Up", font=self.FONT,
                                   command = self.scrollUp)
        self.btn_scrollUp.grid(row=2, column=0, sticky=W + E)
        self.btn_scrollUp.configure(width = 10)
        self.btn_scrollUp.configure(height = 2)
        
        self.btn_scrollDwn = Button(self, text = "Scroll Down", font=self.FONT,
                                   command = self.scrollDwn)
        self.btn_scrollDwn.grid(row=2, column=1, sticky=W + E)
        self.btn_scrollDwn.configure(width = 10)
        self.btn_scrollDwn.configure(height = 2)
        
        
        
        
        
       

    # saves the file using command line 
    def save(self):
        print("chslfjds")
        print(self.fname)
        save = "xdotool search --name {} key ctrl+s".format(self.fname)
        os.system(save)
        print("Saved")
  
   #closes Libre Office using command line 
    def close(self):
        close = "xdotool search --name {} key ctrl+q".format(self.fname)
        os.system(close)
        os.system("sudo pkill soffice.bin") 
        self.destroy()
        self.master.destroy()
        os.killpg(os.getpgid(self.proc1.pid), signal.SIGTERM)
        print("Closed")
        
    #scrolls up using command line 
    def scrollUp(self):
        su = "xdotool search --name {} key Up Up Up Up Up Up Up Up".format(self.fname)
        os.system(su)
    
    #scrolls down using command line
    def scrollDwn(self):
        sd = "xdotool search --name {} key Down Down Down Down Down Down Down Down".format(self.fname)
        os.system(sd)
        



