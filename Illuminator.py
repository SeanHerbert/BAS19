import RPi.GPIO as io
io.setwarnings(False)

class Illuminator(): # Define our class
    def __init__(self,data,clock,bright):
        self.setBrightness(bright)
        self.da = data
        self.ck = clock
        self.on = 0
        io.setmode(io.BCM)
        io.setup(self.ck,io.OUT)
        io.setup(self.da,io.OUT)
        io.output(self.ck, io.HIGH)
        io.output(self.da, io.HIGH)
        self.prevConfig = (self.br<<24)|(255<<16)|(255<<8)|255 
     
    def setBrightness(self,brightness):
        if brightness > 31:
            brightness = 31
        if brightness < 0:
            brightness = 0
        self.br = brightness | 0xE0

    def turnOn(self):
        self.on = 1
        self.led = self.prevConfig
        print(str(self.led))
        self.show()
     
    def changeColor(self,red,green,blue):
        self.led=((self.br<<24)|(red<<16)|(blue<<8)|green)
        if(self.on):
            self.show()
        else:
            self.prevConfig = self.led
        
 
    def show(self):
        io.output(self.da,io.LOW)
        for i in range(0,32): # send header
            io.output(self.ck, io.LOW)
            io.output(self.ck, io.HIGH)
       
            d = self.led # send data
            for j in range(0,32):
                io.output(self.ck, io.LOW)
                if d & 0x80000000 :
                    io.output(self.da, io.HIGH)
                else:
                    io.output(self.da, io.LOW)
                d = d << 1
                io.output(self.ck, io.HIGH)
        io.output(self.da, io.LOW)
        for i in range(0,33): # send footer
            io.output(self.ck, io.LOW)
            io.output(self.ck, io.HIGH)
    def turnOff(self):
        self.on =0
        self.prevConfig = self.led
        self.led = (self.br<<24)|(0<<16)|(0<<8)|0
        self.show()
        

