from FileHandler import FileHandler

#This class runs automatic mode
#It is called from a seperate thread, hence presence of "self.system.control.stop_threads.is_set()" checks 

class Automatic():
    
    #constructor gets system object and filehandler 
    def __init__(self,system):
        self.system = system
        self.fileHandler = FileHandler(self)
        
    #starts autofocus, runs autofocus, then analyzes, then writes results, then moves carousel
    #does that 20 times in a for loop 
    def start(self):
        import time
        start_time = time.time()
        for i in range(20):
            if(self.system.control.stop_threads.is_set()):
                break
            
            #auto focus
            self.system.focus.autoFocus()
            bestImage = self.system.currImage_analyze
#             print("best image found")
            
            if(self.system.control.stop_threads.is_set()):
                break
            
            x = self.system.bloodCounter.countWBC(bestImage)#count WBC's
            
           
            if(self.system.control.stop_threads.is_set()):
                break
            y = self.system.bloodCounter.countRBC(bestImage)#count RBC's
            if(self.system.control.stop_threads.is_set()):
                break
            z = self.system.bloodCounter.calcRatio()#calc WBC:RBC ratio
            if(self.system.control.stop_threads.is_set()):
                break
            pathFlag = self.system.util.pathologyWarn(z)#set pathology flage based on ratio
            
            #send data to main thread via shared queue
            dataArray = ['update_auto',x,y,z,pathFlag,i]
            self.system.GUI.queue.put(dataArray)

            #write results to datafile
            self.fileHandler.writeRatio(self.system.control.wb,self.system.control.ws1,i, z, pathFlag)
            self.fileHandler.writeDateTime(self.system.control.wb,self.system.control.ws1,i)
            self.fileHandler.writePathology(self.system.control.wb,self.system.control.ws1,i,z)
            
            #move carousel to next slide
            self.system.carousel.nextSlide()
            print("moved carousel")
            print("===============================SLIDE {} COMPLETE========================".format(i))
        print("--- %s seconds taken by auto ---" % (time.time() - start_time))
        return 'done'

    
        
        
        
        
    
    

