import numpy as np
import cv2
from scipy import spatial 
from iou import iou

#This Class has the attributes and methods for counting blood cells (WBC's and RBC's) and getting the WBC : RBC ratio
#This class is called in threads, hence the presence of "self.system.control.stop_threads.is_set()" checks througout (for E-stop)

class BloodCounter():
    
    #constructor is passed the system object
    def __init__(self,system):
        self.system = system
        self.wbc_cnt = 0;
        self.rbc_cnt = 0;
        self.ratio= 0;
    
    #simple WBC counter that uses color masking technique to isolate WBC's (WBC's have significantly less red and green than RBC's)
    def countWBC(self,image):
        #this method is called from threads, so it communicates to main thread via a shared queue object
        self.system.GUI.queue.put('removePathBorder')#tells main GUI thread to remove pathology border
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)#convert BGR to HSV
        image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
        #lower and upper bounds for color mask(in HSV)
#         lower_blue = np.array([102,60,218])
#         upper_blue = np.array([148,106,264])
        lower_blue = np.array([200,130,150])
        upper_blue = np.array([255,190,210])
        
        mask = cv2.inRange(image, lower_blue, upper_blue)#mask is in HSV
        res = cv2.bitwise_and(image,image, mask= mask)#res is in BGR
        
        #dilates the detected WBC's to make distinguising between false positives and real WBC's easier 
        kernel_cell = np.ones((5,5),np.uint8)
#         res =cv2.dilate(res, kernel_cell, iterations = 3)
        
        #convert result to HSV and dislay saturation only to pass to removeSmallRegion 
        image_hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
        schan = image_hsv[:,:,1]
        
        #remove small region subtracts false positives from the count and returns the corrected count
        self.wbc_cnt = self.removeSmallRegion(schan) 
        return self.wbc_cnt
    
    #removes false positives based on area
    def removeSmallRegion(self,image):
        min = 9999999
        max = -9999999
        removed = 0
        _,binary = cv2.threshold(image,0,255, cv2.THRESH_BINARY)
#         
        
        if (self.system.control.stop_threads.is_set()):
            return -1
        contours,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            if (self.system.control.stop_threads.is_set()):
                return -1
            area = cv2.contourArea(contours[i])
            if(area >max):
                max = area
            if(area<min):
                min = area
            if area < 40:
                removed+=1
                cv2.drawContours(binary,[contours[i]],0,0,-1)
#         print("~~~~~ITERATION {}~~~~~~~~~".format(k))
        cv2.imwrite("debug/post_process.tif",binary)
        print("min area is: ",min)
        print("max area is: ",max)
        print ("WBC count is: ", len(contours)-removed)
#         return image
        return len(contours)-removed



######################## WENT WITH A SIMPLER COLOR MASKING APPROACH ##############################################################


      #function that counts WBC's using cv2.kmeans clustering, the problem is that cv2.kmeans clustering produced inconsistent results for the
      #same image
#     def countWBC(self,slideImage):
# 
# 
#         self.system.GUI.queue.put('removePathBorder')
#         
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         
#         image_hsv = cv2.cvtColor(slideImage, cv2.COLOR_BGR2HSV)
#         
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         image_s_channel = image_hsv[:,:,1]
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_image = image_s_channel
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_data = cell_image.reshape((-1, 1))
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_data = np.float32(cell_data)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         _,cell_label,cell_center=cv2.kmeans(cell_data,3,None,criteria,1,cv2.KMEANS_RANDOM_CENTERS)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_center = np.uint8(cell_center)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_res = cell_center[cell_label.flatten()]
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell = cell_res.reshape((cell_image.shape))
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         max_v = np.max(cell)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell[cell==max_v] = 255
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell[cell<max_v] = 0
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         kernel_cell = np.ones((5,5),np.uint8)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         processed_cell = self.removeSmallRegion(cell)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
# 
#         
#     
#             
#         processed_cell = cv2.dilate(processed_cell,kernel_cell,iterations = 1)
# 
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cnts,_ = cv2.findContours(processed_cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         cell_num = len(cnts)
#         if (self.system.control.stop_threads.is_set()):
#             return -1
#         #get rid of these after testing
# #         print("There are {} wbc's before remove double".format(cell_num))
#         color = (255, 0, 0)
#         for i in range(cell_num):
#             cnt = cnts[i]
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             x, y, w, h = cv2.boundingRect(cnt)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             slideImage = cv2.rectangle(slideImage, (x, y), (x+w, y+h), color, 2)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
# #             
# # #          cv2.namedWindow("output",cv2.WINDOW_NORMAL)
# #         cv2.imwrite("/home/pi/BAS/testingWBC/After/___{}___{}.tif".format(cell_num,xi),slideImage)
# #         cv2.imwrite("/home/pi/BAS/testingWBC/processed_cell_for_{}___{}.tif".format(cell_num,xi),processed_cell)
# #         image = cv2.resize(slideImage, (1400, 770))   
# # 
# #         cv2.imshow("window", image)
# # 
# #         cv2.waitKey(0)
# # 
# #         cv2.destroyAllWindows()
#             
#             
#         #added for remove double
#         record = []
#         tl_ = []
#         br_ = []
#         iou_ = []
#         iou_value = 0
#             
#         for i in range(cell_num):
# #             if(self.system.control.stop_threads.is_set()):
# #                 return -1
#             if (self.system.control.stop_threads.is_set()):
#                 return -1   
#             cnt = cnts[i]
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             x, y, w, h = cv2.boundingRect(cnt)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             tl =(x,y)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             br = (x+w,y+h)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#                      
#                      #added for remove double count
#             if record != []:
#                 tree = spatial.cKDTree(record)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 index = tree.query(tl)[1]
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_x = int((tl[0] + br[0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_y = int((tl[1] + br[1]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 radius = int((br[0] - tl[0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_x_knn = int((tl_[index][0] + br_[index][0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_y_knn = int((tl_[index][1] + br_[index][1]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 radius_knn = int((br_[index][0] - tl_[index][0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 iou_value = iou(radius,radius_knn,center_x,center_y, center_x_knn,center_y_knn)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 iou_.append(iou_value)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#             if iou_value > 0.02:
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 cell_num = cell_num -1
# #                 print("~~~~~~~~~~~~~~~~~~~~~~~REMOVED~~~~~~~~~~~~~~~~~~~")
#                 continue
#                      
#             record.append(tl)
#             if (self.system.control.stop_threads.is_set()):
#                     return -1
#             tl_.append(tl)
#             if (self.system.control.stop_threads.is_set()):
#                     return -1
#             br_.append(br)
#             if (self.system.control.stop_threads.is_set()):
#                     return -1
#         self.wbc_cnt = cell_num;
# #         print("There are {} wbc's after remove double".format(cell_num))
#         return self.wbc_cnt
# 
# 
#     #removes double counted WBC's using Intersection Over Union and K-nearest Neighbor (to use it, simply pass it the result from
#     #countWBC function)
#     def removeDouble(self,cell_num):
#         
#         record = []
#         tl_ = []
#         br_ = []
#         iou_ = []
#         iou_value = 0
#             
#         for i in range(cell_num):
# 
#             if (self.system.control.stop_threads.is_set()):
#                 return -1   
#             cnt = cnts[i]
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             x, y, w, h = cv2.boundingRect(cnt)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             tl =(x,y)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             br = (x+w,y+h)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#                      
#             
#             if record != []:
#                 tree = spatial.cKDTree(record)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 index = tree.query(tl)[1]
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_x = int((tl[0] + br[0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_y = int((tl[1] + br[1]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 radius = int((br[0] - tl[0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_x_knn = int((tl_[index][0] + br_[index][0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 center_y_knn = int((tl_[index][1] + br_[index][1]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 radius_knn = int((br_[index][0] - tl_[index][0]) / 2)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 iou_value = iou(radius,radius_knn,center_x,center_y, center_x_knn,center_y_knn)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 iou_.append(iou_value)
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#             if iou_value > 0.02:
#                 if (self.system.control.stop_threads.is_set()):
#                     return -1
#                 cell_num = cell_num -1
# #                 print("~~~~~~~~~~~~~~~~~~~~~~~REMOVED~~~~~~~~~~~~~~~~~~~")
#                 continue
#                      
#             record.append(tl)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             tl_.append(tl)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#             br_.append(br)
#             if (self.system.control.stop_threads.is_set()):
#                 return -1
#         self.wbc_cnt = cell_num;
# #         print("There are {} wbc's after remove double".format(cell_num))
#         return self.wbc_cnt

    #counts RBC's using Hough Transform (cv2.HoughCircles). 
    def countRBC(self,slideImage):
        
        if (self.system.control.stop_threads.is_set()):
            print("no image")
            return -1
        gray = cv2.cvtColor(slideImage, cv2.COLOR_BGR2GRAY)
            
            
        
        if (self.system.control.stop_threads.is_set()):
            return -1
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.8, 13, param1 = 60, param2 = 32, minRadius = 6, maxRadius = 15)
        detected_circles = np.uint16(np.around(circles))
#the following draws circles around the detected circles and saves the resultant image (useful for debugging)        
        
#         
#         for i in detected_circles[0,:]:
#             # draw the outer circle
#             cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
#             # draw the center of the circle
#             cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)
#         cv2.imwrite("cirlces.tif",gray)


        self.rbc_cnt = detected_circles.shape[1]
        return self.rbc_cnt
    
    #Calculates WBC to RBC ratio and formats for display on GUI
    def calcRatio(self):
        
        if((self.system.control.stop_threads.is_set())):
            return -1
        self.ratio = self.wbc_cnt/(self.rbc_cnt - self.wbc_cnt)
        self.ratio ="{0:.5f}".format(self.ratio)
        self.ratio = float(self.ratio)
        return self.ratio
        
     
        

        
        
        
