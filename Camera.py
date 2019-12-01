from ximea import xiapi
from CamAdjustFrame import CamAdjustFrame

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import cv2
import numpy as np
import time
import os
from tkinter import *

#this class controls the Ximea camera refer to the ximea API Manual for more detail -> https://www.ximea.com/support/wiki/apis/xiapi_manual
#iamge default size captured by Ximea camera -> width = 4112px , height = 3008px



class Camera():
    def __init__(self,system):
        self.system = system
        self.cam = xiapi.Camera()
        self.cam.open_device()
        
        #camera initial settings
        self.cam.set_imgdataformat('XI_RGB24')
        self.cam.set_exposure(70000)
        self.cam.set_height(900)
        self.cam.set_width(1200)
        self.cam.set_sharpness(4)#set to max sharp
        self.cam.enable_auto_wb()
        #flags and counters 
        self.vidClosed = True
        self.vidPowerCnt = 0
    
    #returns temp in  Celcius 
    def getTemp(self):
        return self.cam.get_temp()
    
    #set sharpness (-4 <= val =< 4)
    def setSharp(self,val):
        self.cam.set_sharpness(val)
        
        
    
    
    
    #used in autofocus to display image to GUI    
    def displayFocusedImage(self):
        self.resizeROI(1200,900)
        img = xiapi.Image()
        self.cam.get_image(img)
        img_analyze = img.get_image_data_numpy()
        self.system.currImage_analyze = img_analyze# image data for analysis is different than for display to GUI 
        img = img.get_image_data_numpy(invert_rgb_order=True)
        img = PIL.Image.fromarray(img, 'RGB')
        self.system.currImage = img
        self.system.imgChange = True #change image flag set for GUI updateImage function 
        return img
        
    #used in autofocus to calculate variance    
    def getImg(self):
        img = xiapi.Image()
        self.cam.get_image(img)

        #create numpy array with data from camera. Dimensions of array are determined
        #by imgdataformat
        img = img.get_image_data_numpy()

        #return acquired image
        
        return img
    
    
    #changes ROI size in pixels (roi is set to upper left corner, there is a way to
    #set ROI position, but was getting errors, refer to API manual)
    def resizeROI(self,width,height):
        self.stopAq()
        self.cam.set_width(width)
        self.cam.set_height(height)
        self.startAq()
        
            
        
    #AqStarted-> returns "XI_ON", AqStopped -> returns "XI_OFF"
    def getAqStatus(self):
        return str(self.cam.get_acquisition_status())
    
    #if on, turn it off
    def startAq(self):
        if(self.getAqStatus() == 'XI_OFF'):
            self.cam.start_acquisition()
            
    #if off, turn it on    
    def stopAq(self):
        if(self.getAqStatus() == 'XI_ON'):
            self.cam.stop_acquisition()
    
    #not currently used 
    def closeCam(self):
        #stop data acquisition
        print('Stopping acquisition...')
        self.stopAq()

        #stop communication
        self.cam.close_device()
    
    #captures image and displays to GUI 
    def showIm(self):
        self.resizeROI(1200,900)
        self.startAq()
        img = xiapi.Image()
        self.cam.get_image(img)
        
        self.system.currImage_analyze = img.get_image_data_numpy()#for analysis 

        #create numpy array with data from camera. Dimensions of array are determined
        #by imgdataformat
        #NOTE: PIL takes RGB bytes in opposite order, so invert_rgb_order is True
        img = img.get_image_data_numpy(invert_rgb_order=True)
        
        
        
        img = PIL.Image.fromarray(img, 'RGB')
        
        self.system.currImage = img
        self.system.imgChange =True
        
        

        #Next 4 lines only for saving image with exposure value

#         d = PIL.ImageDraw.Draw(img)
#         fnt = PIL.ImageFont.truetype('/usr/share/fonts-droid-fallback/truetype/OpenSans-Bold.ttf',100,encoding="unic")
#         d.text((2000,2700),"Exposure: "+str(self.cam.get_exposure()),font = fnt, fill=(255,0,0))
#         img.save('xi_example.tiff')
        
        self.stopAq()
        return img
    
    
    
    
    #this function start the video Thread and keeps it in an infinite loop
    def startVideo(self):
        
        #smaller ROI gets faster frame refresh rate 
        self.resizeROI(400,300) #change to w= 400, h = 300
        self.startAq()
        self.img = xiapi.Image()
        self.data = None
       
        
        #infinite loop for video Thread         
        while True:
            
            time.sleep(0.1) #needed to prevent thread from eating up CPU when video not being displayed
            
            #check parity of video on/off button clicks 
            if(self.vidPowerCnt %2==1):
                
                #set camera settings here. height and width determine ROI size. Aquisition started in GUI function "startVideo()"
                try:
                    self.stopAq()
                    self.cam.set_exposure(70000)#this is a good value for current setup
                    self.startAq()
                    self.resizeROI(400,300)#change back to small ROI if not already small

                
                except:
                    
                    print("can't set camera params")
                    
                self.vidClosed = False # set vidClosed Flag to False on odd parity on/off buton click count
                
                
            while (self.vidPowerCnt %2==1):
                
                self.startAq()
                        
                #get data and pass them from camera to img
                self.cam.get_image(self.img,100000)#second param is timeout (set really long just in case)
                    
                #create numpy array with data from camera. Dimensions of the array are 
                #determined by imgdataformat
                self.data = self.img.get_image_data_numpy()
                
                #calculate variance for image sharpness and display to frame
#                 var = self.system.focus.varianceofLap(self.data) #can use this cv2.variance if wanted instead 
               
                var =np.var(self.data) #using numpy variance currently 
                var = '{:5.2f}'.format(var)
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                #put variance reading on video frame for easier manual focusing 
                cv2.putText(
                        self.data, var, (0,100), font, 4, (255, 0, 0), 2   #currently using blue text color
                        )
 
                if(self.data is None):
                    print("no data")
                cv2.imshow('XiCAM Video', self.data)
                cv2.waitKey(20) #number of milliseconds frame is displayed 
                
                #position window and set it to stay on top    
                cv2.moveWindow("XiCAM Video", 1400,200)
                os.system("wmctrl -r 'XiCAM Video' -b add,above")
                
     
            #destroy window and stop camera acquisition, set vidClosed flage to True
            if (self.vidClosed == False):
                self.vidClosed = True
                
                cv2.destroyWindow('XiCAM Video')
        
                self.stopAq()

    #generates the cam adjust window     
    def camAdjust(self):
        r = Tk()
        r.geometry("450x875+760+10")
        r.call('wm', 'attributes', '.', '-topmost', '1') #keeps the window on top
        r.title("Cam Adjust")
        r.configure(background = "blue")#used for contrasting background
        r.overrideredirect(True) #remove minimize and exit toolbar from window
        
        #generate camera Adjust window    
        self.caf = CamAdjustFrame(r,self.system)
    
    #closes window
    def camAdjustExit(self):
        self.caf.cafExit()
    
    #enables auto white balance mode
    def enableAutoWB(self):
        self.cam.enable_auto_wb()
        print("enabled awb")
        
    #enables auto white balance mode
    def disableAutoWB(self):
        self.cam.disable_auto_wb()
        self.setManWB(1.0,1.0,1.0) #resets white balance coeffients to all 1.0
        print("disabled awb")
        
    #sets manual white balance values (0.0 - 10.0)   
    def setManWB(self,r,g,b):
        self.cam.set_wb_kr(r)
        self.cam.set_wb_kg(g)
        self.cam.set_wb_kb(b)
    
    #doesn't work, camera hasn't adjustable lens
    def setAperture(self,val):
        self.cam.enable_lens_mode()
        self.cam.set_lens_aperture_value(val)
        
        
        
        
    #not used currently(only works with cv2 images)   
    def ResizeWithAspectRatio(self,image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)
        


        
    