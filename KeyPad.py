

from tkinter import *


class KeyPad(Frame):
    """ GUI frame with a text box and keypad """

    def __init__(self, master,GUI,caller):
        
        """ initialize the frame """
        self.GUI = GUI
        
        if(self.GUI.kpRunning==0):
            self.GUI.kpRunning=1
            print(self.GUI.kpRunning)
            self.master = master
            self.caller = caller
            print (self.caller)
            self.width =7000
            super(KeyPad, self).__init__(master)
            self.grid()
            
#             self.geometry("1920x1050+385+327")
            self.FONT = ("times bold", "20")
            self.current_digit = 0
            self.create_widgets()
            
            self.caller.config(state=DISABLED)

    def create_widgets(self):
        """ Create the buttons for the keypad """

        self.txt_prompt = Text(self, width=10, height=5, font=self.FONT)
        self.txt_prompt.grid(row=0, column=0, columnspan=3, sticky=W + E)
        self.txt_prompt.config(state=DISABLED)

        # Create row 1 buttons
        self.btn_seven = Button(self, text="7", font=self.FONT,
                                command=lambda: self.digit("7"))
        self.btn_seven.grid(row=1, column=0, sticky=W + E)
        self.btn_seven.configure(width = 10)
        self.btn_seven.configure(height = 5)


        self.btn_eight = Button(self, text="8", font=self.FONT,
                                command=lambda: self.digit("8"))
        self.btn_eight.grid(row=1, column=1, sticky=W + E)
        self.btn_eight.configure(width = 10)
        self.btn_eight.configure(height = 5)
        
        self.btn_nine = Button(self, text="9", font=self.FONT,
                               command=lambda: self.digit("9"))
        self.btn_nine.grid(row=1, column=2, sticky=W + E)
        self.btn_nine.configure(width = 10)
        self.btn_nine.configure(height = 5)
        # Create row 2 buttons
        self.btn_four = Button(self, text="4", font=self.FONT,
                               command=lambda: self.digit("4"))
        self.btn_four.grid(row=2, column=0, sticky=W + E)
        self.btn_four.configure(width = 10)
        self.btn_four.configure(height = 5)
        self.btn_five = Button(self, text="5", font=self.FONT,
                               command=lambda: self.digit("5"))
        self.btn_five.grid(row=2, column=1, sticky=W + E)
        self.btn_five.configure(width = 10)
        self.btn_five.configure(height = 5)
        self.btn_six = Button(self, text="6", font=self.FONT,
                              command=lambda: self.digit("6"))
        self.btn_six.grid(row=2, column=2, sticky=W + E)
        self.btn_six.configure(width = 10)
        self.btn_six.configure(height = 5)
        # Create row 3 buttons
        self.btn_one = Button(self, text="1", font=self.FONT,
                              command=lambda: self.digit("1"))
        self.btn_one.grid(row=3, column=0, sticky=W + E)
        self.btn_one.configure(width = 10)
        self.btn_one.configure(height = 5)
        self.btn_two = Button(self, text="2", font=self.FONT,
                              command=lambda: self.digit("2"))
        self.btn_two.grid(row=3, column=1, sticky=W + E)
        self.btn_two.configure(width = 10)
        self.btn_two.configure(height = 5)
        self.btn_three = Button(self, text="3", font=self.FONT,
                                command=lambda: self.digit("3"))
        self.btn_three.grid(row=3, column=2, sticky=W + E)
        self.btn_three.configure(width = 10)
        self.btn_three.configure(height = 5)
        # Create 0, decimal, and enter buttons
        self.btn_zero = Button(self, text="0", font=self.FONT,
                               command=lambda: self.digit("0"))
        self.btn_zero.grid(row=4, column=0, columnspan=2, sticky=W + E)
        self.btn_zero.configure(height = 5)

        self.btn_decimal = Button(self, text=".", font=self.FONT,
                                command=lambda: self.digit("."))
        self.btn_decimal.grid(row=4, column=2,  sticky=W + E)
        self.btn_decimal.configure(width = 10)
        self.btn_decimal.configure(height = 5)
        self.btn_enter = Button(self, text="Enter", font=self.FONT,
                                 command=self.enter)
        self.btn_enter.grid(row=5, column=0, columnspan=3, sticky=W + E)
        self.btn_enter.configure(height = 5)

        # updates the buttons

    def digit(self, new_digit):
        self.prompt = self.txt_prompt.get(0.0, END).strip()
        self.current_digit = new_digit
        
        self.update_box()

    # updates the text box with input from the buttons
    def update_box(self):
        self.txt_prompt.config(state=NORMAL)
        self.txt_prompt.insert(END, self.current_digit)
        
   #kills window and inserts entered text into the widget that called from, also validates and bounds input
    def enter(self):
        input = float(self.txt_prompt.get("1.0",END))
        if "labelframe7" in str(self.caller):
            input = int(input)
            if(input>255):
                input = 255
        if "labelframe8" in str(self.caller):
            input = int(input)
            if(input>19):
                input=19
            if(input<0):
                input =0
        if "camadjustframe.!labelframe2" in str(self.caller):
            input = int(input)
            print("here")
        if "camadjustframe.!labelframe3" in str(self.caller):
            if(input>8):
                input=19
            if(input<0):
                input =0
            input = float(input)
            
        self.caller.config(state=NORMAL)
        self.caller.delete("1.0", "end")
        self.caller.insert(END,input)
        self.destroy()
        self.quit()
        self.master.destroy()
        self.master.quit()
        self.GUI.kpRunning =0

 

