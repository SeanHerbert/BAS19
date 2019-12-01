import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import sys
from scipy import spatial 
from iou import iou
import time
image1 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\BAS19\Images\10x Slide 520030747 second spot in-focus height 84um.tif", 1)
image2 = cv2.imread(r"xi_example.tiff", 1)

image3 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\Blood Cell Images from Roche/10x-Slide-520030762-in-focus-height-64um.tif", 1)

image4 = cv2.imread(r"C:\Users\Sean Herbert\Desktop\Fall2019\Senior project\Blood Cell Images from Roche/10x-Slide-520030762-in-focus-height-64um.tif", 1)


def removeSmallRegion(image, size):
    removed = 0
    _,binary = cv2.threshold(image,0,255, cv2.THRESH_BINARY)
    
    contours, hierarch = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
#         print(area)
        if area < size:
            removed +=1
            
    
            
#     cv2.imwrite("debug/debug_{}.tif".format(str(k)),image)
    
#     cv2.imshow("Image",image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    return len(contours)-removed



def test(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([102,60,218])
    upper_blue = np.array([148,106,264])
    mask = cv2.inRange(image_hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(image,image, mask= mask)
    kernel_cell = np.ones((5,5),np.uint8)
    res =cv2.dilate(res, kernel_cell, iterations = 2)
    image_hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    schan = image_hsv[:,:,1]
    cv2.imwrite("im.tiff",schan)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cnt = removeSmallRegion(schan,100)
    print(cnt)
    
#     cnts,hierarchy = cv2.findContours(schan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # Setup SimpleBlobDetector parameters.
#     print(len(cnts))
#     gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.8, 13, param1 = 60, param2 = 32, minRadius = 6, maxRadius = 50)
#     cv2.imshow("Im",res)
#     cv2.waitKey(0)
#     detected_circles = np.uint16(np.around(circles))
#     self.rbc_cnt = detected_circles.shape[1];
#     return self.rbc_cnt
    


def process_img(image,i):
#     dark_red  = np.uint8([[[241,163,176]]])
#     dark_red = cv2.cvtColor(dark_red,cv2.COLOR_BGR2HSV)
#     print(dark_red)
    
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_s_channel = image_hsv[:,:,1]
    cell_image = image_s_channel.copy();


#expiremental
#     cv2.imshow('im',image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    
 #     detector = cv2.SimpleBlobDetector()
 
    # Detect blobs.
#     keypoints = detector.detect(res)
     
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
#     im_with_keypoints = cv2.drawKeypoints(res, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     
    # Show keypoints
#     cv2.imshow("Keypoints", im_with_keypoints)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     image_hsv=cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
#     image_s_channel = image_hsv[:,:,1]
#     cell_image = image_s_channel.copy()
#     cv2.imwrite("debug/Masked.tif",cell_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    
# 
#     
#     cv2.imwrite("debug/cell_image{}.tif".format(str(i)),image_s_channel)
    
    
    cell_data = cell_image.reshape((-1, 1))
    
    cell_data = np.float32(cell_data)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30, 0.1)
    cell_ret,cell_label,cell_center=cv2.kmeans(cell_data,3,None,criteria,1,cv2.KMEANS_RANDOM_CENTERS)
    cell_center = np.uint8(cell_center)
    
    cell_res = cell_center[cell_label.flatten()]
    
    cell = cell_res.reshape((cell_image.shape))
    
    max_v = np.max(cell)
    cell[cell==max_v] = 255
    cell[cell<max_v] = 0
    
    
    kernel_cell = np.ones((5,5),np.uint8)
    processed_cell = removeSmallRegion(cell, 306.5,i)

    processed_cell = cv2.dilate(processed_cell,kernel_cell,iterations = 1)


    color = (255, 0, 0)
    cnts,hierarchy = cv2.findContours(processed_cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     print(cnts)
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
#          print(tl)
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
#             print("The KNN for {} is {}".format(tl,tl_[index]))
#             print("The iou_value for {} is {}".format(tl,iou_value))
            iou_.append(iou_value)
         if iou_value > 0.02:
            cell_num = cell_num -1
            print("removed", tl)
            continue
         center_x = int((tl[0] + br[0]) / 2)
         center_y = int((tl[1] + br[1]) / 2)
         center = (center_x, center_y)
         radius = int((br[0] - tl[0]) / 2)
#          image = cv2.circle(image, center, radius, color, 2)

#          print("printed",tl)
         record.append(tl)
         tl_.append(tl)
         br_.append(br)


    print("white cell number: ", cell_num)

    
    # cv2.namedWindow("output",cv2.WINDOW_NORMAL) 
    # image = cv2.resize(image, (1400, 770))    
    # cv2.imshow("window", image)
    # cv2.waitKey(0)
    
for i in range (50):
    
    imageTemp = image2
    test(imageTemp)
#     cv2.imshow("Image",image2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     process_img(imageTemp,i)
    