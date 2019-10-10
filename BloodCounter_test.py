from BloodCounter import BloodCounter
from System import System
import cv2
import time

system =System(3)
bc = BloodCounter(system)
# bc1 = BloodCounter(system)
# bc2 = BloodCounter(system)
# bc3 = BloodCounter(system)
# bc4 = BloodCounter(system)
# bc5 = BloodCounter(system)
# bc6 = BloodCounter(system)
# bc7 = BloodCounter(system)
# bc8 = BloodCounter(system)
# bc9 = BloodCounter(system)
# bc10 = BloodCounter(system)

image = cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif")
for i in range(20):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~~~~~~~~~~~~~~~~~~~~~~~~~".format(i))
    bc.countWBC(image,i)
#     time.sleep(3)
# bc1.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc2.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc3.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc4.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc5.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc6.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc7.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc8.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc9.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc10.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))
# bc.countWBC(cv2.imread("/home/pi/BAS/Images/i12/10x Slide 520030762 in-focus height 64um.tif"))

# bc.countRBC(image)
# bc.calcRatio()

# print("{} red blood cells and {} white blood cells detected\nwbc/rbc ratio is {}".format(bc.rbc_cnt,bc.wbc_cnt,bc.ratio))

