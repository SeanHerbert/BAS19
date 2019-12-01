from BloodCounter import BloodCounter
import cv2

b = BloodCounter()

b.countWBC(cv2.imread("/home/pi/BAS/xi_example.tiff"))