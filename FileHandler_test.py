from FileHandler import FileHandler
from System import System

s = System(3)
f = FileHandler(s)
f.createNewDataFile()
f.openCurrentDataFile()
