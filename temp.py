#!/usr/bin/python

import cv2.cv as cv
import cv2
import numpy as np
import time
from datetime import datetime

class benchmarke:
    def __init__(self):
        self.prevTime = datetime.now()
        
    def stopp(self):
             dt = datetime.now()
             diff = dt - self.prevTime
             print "Diff:" , diff, " FPS:", float(1000000/(diff.microseconds))
             self.prevTime = dt 


cap = cv2.VideoCapture(0)
cap.set(5, 90)
bench = benchmarke()

while True:
    flag , frame = cap.read() 
    cv2.imshow("test",frame)
    cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    bench.stopp()
    if cv.WaitKey(10) == 27:
        break
cv.DestroyAllWindows()
