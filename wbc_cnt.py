import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import sys
from scipy import spatial 
from iou import iou
image1 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\BAS19\Images\10x Slide 520030747 second spot in-focus height 84um.tif", 1)
image2 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\BAS19\Images\10x Slide 520030747 third spot in-focus height 84um.tif", 1)

image3 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\Blood Cell Images from Roche/10x-Slide-520030762-in-focus-height-64um.tif", 1)

image4 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\Blood Cell Images from Roche/10x-Slide-520030762-in-focus-height-64um.tif", 1)


def removeSmallRegion(image, size):
    _,binary = cv2.threshold(image,100,255, cv2.THRESH_BINARY)
    
    contours, hierarch = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < size:
            cv2.drawContours(image,[contours[i]],0,0,-1)

    return image

def process_img(image):

 
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
    processed_cell = removeSmallRegion(cell, 100)
    
    processed_cell = cv2.dilate(processed_cell,kernel_cell,iterations = 1)


    color = (255, 0, 0)
    cnts,hierarchy = cv2.findContours(processed_cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cell_num = len(cnts)
    cell_area = 0
    
    #added for remove double
    record = []
    tl_ = []
    br_ = []
    iou_ = []
    iou_value = 0
    z = 0
    
    for i in range(cell_num):
    
        
    
         cell_area += cv2.contourArea(cnts[i])
         cnt = cnts[i]
         x, y, w, h = cv2.boundingRect(cnt)
         tl =(x,y)
         print(tl)
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
            print("The KNN for {} is {}".format(tl,tl_[index]))
            print("The iou_value for {} is {}".format(tl,iou_value))
            iou_.append(iou_value)
         if iou_value > 0.02:
            cell_num = cell_num -1
            print("removed", tl)
            continue
         center_x = int((tl[0] + br[0]) / 2)
         center_y = int((tl[1] + br[1]) / 2)
         center = (center_x, center_y)
         radius = int((br[0] - tl[0]) / 2)
         image = cv2.circle(image, center, radius, color, 2)

         print("printed",tl)
         record.append(tl)
         tl_.append(tl)
         br_.append(br)

 
    print("white cell number: ", cell_num)


    cv2.imshow("Image",image)
    cv2.waitKey(0)
    # cv2.namedWindow("output",cv2.WINDOW_NORMAL) 
    # image = cv2.resize(image, (1400, 770))    
    # cv2.imshow("window", image)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

process_img(image=image2)