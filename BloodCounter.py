import numpy as np
import cv2
from scipy import spatial 
from iou import iou

class BloodCounter():
    def __init__(self):
        self.wbc_cnt = 0;
        self.rbc_cnt = 0;
        self.ratio= 0; 

    def removeSmallRegion(self,image):
        _,binary = cv2.threshold(image,100,255, cv2.THRESH_BINARY)
        
        contours, hierarch = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area < 95:
                cv2.drawContours(image,[contours[i]],0,0,-1)

        return image

    def countWBC(self,slideImage):
        slideImage = cv2.imread(slideImage,1)
        image_hsv = cv2.cvtColor(slideImage, cv2.COLOR_BGR2HSV)
        image_s_channel = image_hsv[:,:,1]
        cell_image = image_s_channel;
        cell_data = cell_image.reshape((-1, 1))
        cell_data = np.float32(cell_data)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)
        cell_ret,cell_label,cell_center=cv2.kmeans(cell_data,3,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        cell_center = np.uint8(cell_center)
        cell_res = cell_center[cell_label.flatten()]
        cell = cell_res.reshape((cell_image.shape))
        max_v = np.max(cell)
        cell[cell==max_v] = 255
        cell[cell<max_v] = 0

        kernel_cell = np.ones((5,5),np.uint8)
        processed_cell = self.removeSmallRegion(cell)
        
        processed_cell = cv2.dilate(processed_cell,kernel_cell,iterations = 1)


        cnts,hierarchy = cv2.findContours(processed_cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cell_num = len(cnts)
        
        
        #added for remove double
        record = []
        tl_ = []
        br_ = []
        iou_ = []
        iou_value = 0
        
        for i in range(cell_num):
        
            
        
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
                continue
             
             record.append(tl)
             tl_.append(tl)
             br_.append(br)
        self.wbc_cnt = cell_num;
        return self.wbc_cnt

    def countRBC(self,slideImage):
        
        slideImage = cv2.imread(slideImage,1)
        gray = cv2.cvtColor(slideImage, cv2.COLOR_BGR2GRAY)
        

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.8, 13, param1 = 60, param2 = 32, minRadius = 6, maxRadius = 10)

        detected_circles = np.uint16(np.around(circles))
        self.rbc_cnt = detected_circles.shape[1];
        return self.rbc_cnt
    def calcRatio(self):
        self.ratio = self.wbc_cnt/(self.rbc_cnt - self.wbc_cnt)
        self.ratio ="{0:.5f}".format(self.ratio)
        return self.ratio
        
     
        

        
        
        