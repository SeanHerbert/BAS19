import time
from Utility import Utility

u =Utility()
# u.createNewDataFile()
# time.sleep(20)
# u.openCurrentDataFile()
u.setPathology(.0001,.005)
print(u.pathologyWarn(.003))
