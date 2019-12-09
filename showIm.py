import cv2
import numpy as np

x = cv2.imread('thePic.tif')
lower_red = np.array([200,130,150])
upper_red = np.array([255,190,210])
    
mask = cv2.inRange(x, lower_red, upper_red)
res = cv2.bitwise_and(x,x, mask= mask)
# kernel_cell = np.ones((5,5),np.uint8)
# res =cv2.dilate(res, kernel_cell, iterations = 1)
image_hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
schan = image_hsv[:,:,1]




min = 9999999
max = -9999999
removed = 0
_,binary = cv2.threshold(schan,0,255, cv2.THRESH_BINARY)
#         cv2.imwrite("debug/post_process_{}.tif".format(k),binary)
        

contours,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    
    area = cv2.contourArea(contours[i])
    print(area)
    if(area >max):
        max = area
        

        
    if(area<min):
        if(not area == 0):
            min = area
        

    if area < 70:
        removed+=1
        cv2.drawContours(binary,[contours[i]],0,0,-1)
cv2.imwrite('b.tif',binary)

print ("WBC count is: ", len(contours)-removed)





