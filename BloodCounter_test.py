from BloodCounter import BloodCounter
bc = BloodCounter()
bc.countWBC("/home/pi/BAS/Images/i13/10x Slide 520030747 third spot in-focus height 84um.tif")
bc.countRBC("/home/pi/BAS/Images/i13/10x Slide 520030747 third spot in-focus height 84um.tif")
bc.calcRatio()

print("{} red blood cells and {} white blood cells detected\nwbc/rbc ratio is {}".format(bc.rbc_cnt,bc.wbc_cnt,bc.ratio))

