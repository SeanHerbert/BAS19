import numpy as np
import cv2
from scipy import spatial 
from iou import iou
import random

class BloodCounter():
    def __init__(self,system):
        self.system = system
        self.wbc_cnt = 0;
        self.rbc_cnt = 0;
        self.ratio= 0;
        

    def removeSmallRegion(self,image):
#         binary=0
#         contours=0
#         hierarch=0
#         area=0
        _,binary = cv2.threshold(image,100,255, cv2.THRESH_BINARY)
        

        if (self.system.control.stop_threads.is_set()):
            return -1
        contours,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            if (self.system.control.stop_threads.is_set()):
                return -1
            area = cv2.contourArea(contours[i])
            if area < 80:
                cv2.drawContours(image,[contours[i]],0,0,-1)
#         cv2.imwrite("/home/pi/BAS/testingWBC/processed_cell_for_{}.tif".format(j),image)
        return image

    def countWBC(self,slideImage):
        #remove pathology out of bounds red border at the beggining of each new analysis
        xi=random.random()
        cv2.imwrite("/home/pi/BAS/testingWBC/Before/___{}.tif".format(xi),slideImage)


        self.system.GUI.removePathologyBorder()

        if (self.system.control.stop_threads.is_set()):
            return -1
        image_hsv = cv2.cvtColor(slideImage, cv2.COLOR_BGR2HSV)
        image_s_channel = image_hsv[:,:,1]
        cell_image = image_s_channel;
        cell_data = cell_image.reshape((-1, 1))
        cell_data = np.float32(cell_data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
        if (self.system.control.stop_threads.is_set()):
            return -1
        _,cell_label,cell_center=cv2.kmeans(cell_data,3,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        cell_center = np.uint8(cell_center)
        cell_res = cell_center[cell_label.flatten()]
        cell = cell_res.reshape((cell_image.shape))
        max_v = np.max(cell)
        cell[cell==max_v] = 255
        cell[cell<max_v] = 0
        if (self.system.control.stop_threads.is_set()):
            return -1
        kernel_cell = np.ones((5,5),np.uint8)
#         print(kernel_cell)
        processed_cell = self.removeSmallRegion(cell)
#         xi=random.random()

        
    
            
        processed_cell = cv2.dilate(processed_cell,kernel_cell,iterations = 1)

        if (self.system.control.stop_threads.is_set()):
            return -1
        cnts,_ = cv2.findContours(processed_cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cell_num = len(cnts)
        #get rid of these after testing
        print("There are {} wbc's before remove double".format(cell_num))
        color = (255, 0, 0)
        for i in range(cell_num):
            cnt = cnts[i]
            x, y, w, h = cv2.boundingRect(cnt)
            slideImage = cv2.rectangle(slideImage, (x, y), (x+w, y+h), color, 2)
#             
# #          cv2.namedWindow("output",cv2.WINDOW_NORMAL)
        cv2.imwrite("/home/pi/BAS/testingWBC/After/___{}___{}.tif".format(cell_num,xi),slideImage)
#         cv2.imwrite("/home/pi/BAS/testingWBC/processed_cell_for_{}___{}.tif".format(cell_num,xi),processed_cell)
#         image = cv2.resize(slideImage, (1400, 770))   
# 
#         cv2.imshow("window", image)
# 
#         cv2.waitKey(0)
# 
#         cv2.destroyAllWindows()
            
            
        #added for remove double
        record = []
        tl_ = []
        br_ = []
        iou_ = []
        iou_value = 0
            
        for i in range(cell_num):
            if(self.system.control.stop_threads.is_set()):
                return -1
                
            cnt = cnts[i]
            x, y, w, h = cv2.boundingRect(cnt)
            tl =(x,y)
            br = (x+w,y+h)
                     
                     #added for remove double count
            if record != []:
                tree = spatial.cKDTree(record)
                index = tree.query(tl)[1]
                center_x = int((tl[0] + br[0]) / 2)
                center_y = int((tl[1] + br[1]) / 2)
                radius = int((br[0] - tl[0]) / 2)
                center_x_knn = int((tl_[index][0] + br_[index][0]) / 2)
                center_y_knn = int((tl_[index][1] + br_[index][1]) / 2)
                radius_knn = int((br_[index][0] - tl_[index][0]) / 2)
                iou_value = iou(radius,radius_knn,center_x,center_y, center_x_knn,center_y_knn)
                iou_.append(iou_value)
            if iou_value > 0.02:
                cell_num = cell_num -1
                print("~~~~~~~~~~~~~~~~~~~~~~~REMOVED~~~~~~~~~~~~~~~~~~~")
                continue
                     
            record.append(tl)
            tl_.append(tl)
            br_.append(br)
        self.wbc_cnt = cell_num;
        print("There are {} wbc's after remove double".format(cell_num))
        return self.wbc_cnt

    def countRBC(self,slideImage):
        
#         slideImage = cv2.imread(slideImage,1)
        if (self.system.control.stop_threads.is_set()):
            print("no image")
            return -1
        gray = cv2.cvtColor(slideImage, cv2.COLOR_BGR2GRAY)
            
            
        
        if (self.system.control.stop_threads.is_set()):
            return -1
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.8, 13, param1 = 60, param2 = 32, minRadius = 6, maxRadius = 10)
        detected_circles = np.uint16(np.around(circles))
        self.rbc_cnt = detected_circles.shape[1];
        return self.rbc_cnt
        
    def calcRatio(self):
        if((self.system.control.stop_threads.is_set())):
            return -1
        self.ratio = self.wbc_cnt/(self.rbc_cnt - self.wbc_cnt)
        self.ratio ="{0:.5f}".format(self.ratio)
        self.ratio = float(self.ratio)
        
        if(self.ratio<self.system.util.minPathology or self.ratio >self.system.util.maxPathology):
            self.system.GUI.addPathologyBorder()
            
        return self.ratio
        
     
        

        
        
        
