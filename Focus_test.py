import cv2
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from imutils import paths
from Focus import Focus

f = Focus()
f.autoFocus()

