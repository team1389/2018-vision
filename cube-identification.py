#!/usr/bin/env python
import cv2
import numpy as np
import os
from networktables import NetworkTables


# Restore defaults for cam
os.system('v4l2-ctl -c exposure=12q0')
os.system('v4l2-ctl -c contrast=32')
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)


#HSV Values
lower = np.array([25, 80, 120])
upper = np.array([70, 185, 255])
	
#Erosion
erosionKernel = np.ones((3,3), np.uint8)
dilateKernel = np.ones((0,0), np.uint8)

#Network Tables
NetworkTables.initialize('10.13.89.99') 
sd = NetworkTables.getTable('vision')
cap = cv2.VideoCapture(0)
i = 0

#Loop
while(True):
	error = 0
        
	#reading every frame
	ret, img = cap.read()
	default = img
	height, width = img.shape[:2]
	
	#increased upper HSV vals	
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
	
	# Convert the image from RGB to HSV color space.  This is required for the next operation.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
	# Create a new image that contains yellow where the color was detected
	img = cv2.inRange(hsv, lower, upper)
	img = cv2.erode(img, erosionKernel, iterations =1)
	img = cv2.dilate(img, dilateKernel, iterations=1)

	# Blurring operation helps forthcoming contours work better
	img= cv2.blur(img, (3,3))
	    
	# Find contours
	(_, cnts, _) = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    

	# Makes the first contour the largest
	contours = sorted(cnts, key = cv2.contourArea, reverse = True)

	# If no contours are detected, then don't try to process them or you'll get an error:
	if len(contours) > 0:
		cnt1 = contours[0]
		area = cv2.contourArea(cnt1)
		
		# Draw a minimum area rectangle around the contour
		rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
		
		# Draw the contour over image
		cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
		M1 = cv2.moments(cnt1)
		cx1 = int(M1['m10']/M1['m00'])
		
		#draw center of cube on image in red

		#display center of image on img in white
		centX = int(width/2)
		centY = int(height/2)

		#error to be sent over network tables
		error = centX - cx1
		if area < 200:
                       error = 0 
		cv2.circle(img, (centX, centY),30, (255,255,255))

	cv2.imshow('frame', img) 
	sd.putNumber('error', error)
	

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
