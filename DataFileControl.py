

from tkinter import *
import os
import subprocess
import signal



class DataFileControl(Frame):
    """ GUI frame with a text box and keypad """

    def __init__(self, master,system):
        
        """ initialize the frame """
        
#         if(self.GUI.kpRunning==0):
#             self.GUI.kpRunning=1
#             print(self.GUI.kpRunning)
        self.fname = system.dataFilePaths[system.currFileIndex][23:]
        self.master = master
        super(DataFileControl, self).__init__(master)
        self.grid()
            
#             self.geometry("1920x1050+385+327")
        self.FONT = ("times bold", "20")
        self.create_buttons()
        self.proc1 = subprocess.Popen("florence",shell=True,preexec_fn=os.setsid)
            

    def create_buttons(self):

               # Create row 1 buttons
        self.btn_save = Button(self, text="Save", font=self.FONT,
                                command=self.save)
        self.btn_save.grid(row=1, column=0, sticky=W + E)
        self.btn_save.configure(width = 10)
        self.btn_save.configure(height = 4)


        self.btn_close = Button(self, text="Close", font=self.FONT,
                                command=self.close)
        self.btn_close.grid(row=1, column=1, sticky=W + E)
        self.btn_close.configure(width = 10)
        self.btn_close.configure(height = 4)
        
        
        
        
        
       

        # updates the buttons
    def save(self):
        save = "xdotool search --name {} key ctrl+s".format(self.fname)
        os.system(save)
        print("Saved")
  
   #kills window and inserts entered text into the widget that called from, also validates and bounds input
    def close(self):
        
        
        close = "xdotool search --name {} key ctrl+q".format(self.fname)
        os.system(close)
        os.system("sudo pkill soffice.bin") 
        self.destroy()
        self.master.destroy()
        os.killpg(os.getpgid(self.proc1.pid), signal.SIGTERM)
        print("Closed")
#         self.GUI.kpRunning =0
# r = Tk()
# r.geometry("400x120+1520+0")
# r.call('wm', 'attributes', '.', '-topmost', '1') #keeps the keypad on top
# r.title("Save/Close")
#             
# dfc = DataFileControl(r,self.system)
# dfc.grid()
# r.mainloop()
 


