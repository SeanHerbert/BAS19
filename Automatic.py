from carousel import carousel
from Focus import Focus
from BloodCounter import BloodCounter

class Automatic():
    def __init__(self,system):
        self.system = system
        self.carousel = carousel()
        self.focus = Focus()
        self.bloodCounter = BloodCounter()
        
    def start(self):
        for i in range(20):
            #auto focus
            bestImage = self.focus.autoFocus()
            #analyze image
            self.bloodCounter.countWBC(bestImage)
            self.bloodCounter.countRBC(bestImage)
            self.bloodCounter.calcRatio()
            #pass bloodCounter.wbc_cnt to GUI
            print("wbc's is ", self.bloodCounter.wbc_cnt)
            #pass bloodCounter.rbc_cnt to GUI
            print("rbc's is ", self.bloodCounter.rbc_cnt)
            #pass bloodCounter.ratio to GUI
            print("ratio is ", self.bloodCounter.ratio)
            self.carousel.nextSlide()
        
        
    
    