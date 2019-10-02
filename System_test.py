from System import System
import time


sys = System()
sys.util.createNewDataFile()
print(sys.currFileIndex)
time.sleep(10)
sys.util.openCurrentDataFile()
sys.auto.start()
# s.util.dataEnter()