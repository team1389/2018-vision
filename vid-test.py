import numpy as np
import cv2
cap = cv2.VideoCapture(0)
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
while(True):
    ret, img = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
    cv2.imshow('frame', img)
