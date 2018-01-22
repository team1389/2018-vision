#!/usr/bin/python

import numpy as np
import cv2
import os
#working with some noise using ps eye on pi, with lighting from above
#determined that I couldn't pick up both directly illuminated and semi-illuminated surfaces, this is tuned for semi-illuminated
#28 inches for arm from center of robot to end
#minimum distance to pick up well is 21 inches with [28, 40, 125] - [75, 175, 230]

#restore defaults for cam
os.system('v4l2-ctl -c exposure=12q0')
os.system('v4l2-ctl -c contrast=32')
#setting up size of display
wnd = 'HSVBars'
lh = 'Lower Hue'
uh = 'Upper Hue'
ls = 'Lower Saturation'
us = 'Upper Saturation'
lv = 'Lower Value'
uv = 'Upper Value'
cv2.namedWindow('HSVBars', cv2.WINDOW_NORMAL)
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 100,100)
#Lower Trackbars
#15,25,153])  # HSV
        #upper = np.array([100,102,204
cv2.createTrackbar(lh, wnd, 27, 179, lambda:none)
cv2.createTrackbar(ls, wnd, 40, 255, lambda:none)
cv2.createTrackbar(lv, wnd, 123, 255, lambda:none)

#Upper Trackbars
cv2.createTrackbar(uh, wnd, 75, 179, lambda:none)
cv2.createTrackbar(us, wnd, 175, 255, lambda:none)
cv2.createTrackbar(uv, wnd, 233, 255, lambda:none)	
#could increase erosion to deal with picking up brighter shades,but as it increases, we lose our ability to pick up sides not facing the cam directly
erosionKernel = np.ones((5,5), np.uint8)
dilateKernel = np.ones((1,1), np.uint8)

#as we raise S value, we stop registering brighter shades
#determine how important seeing said brighter shades
#at current vals, unable to see side being illuminated from most angles


cap = cv2.VideoCapture(0)
count = 0
while(True):
        #Read trackbar changes
	lowh = cv2.getTrackbarPos(lh, wnd)
	lows = cv2.getTrackbarPos(ls, wnd)
	lowv = cv2.getTrackbarPos(lv, wnd)
	
	uph = cv2.getTrackbarPos(uh, wnd)
	ups = cv2.getTrackbarPos(us, wnd)
	upv = cv2.getTrackbarPos(uv, wnd)

	#setting up size of display window 
	#reading every frame
	ret, img = cap.read()
	default = img
	height, width = img.shape[:2]
	
	#increased upper HSV vals	
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
	    # Our operations on the frame come here
	    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    # cv2.imshow('frame', img)

	    # Convert the image from RGB to HSV color space.  This is required for the next operation.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #lower = np.array([15,25,153])  # HSV
        #upper = np.array([100,102,204])
	lower = np.array([lowh, lows, lowv])
	upper = np.array([uph, ups, upv])
	    # Create a new image that contains yellow where the color was detected, otherwise purple? or black?
	img = cv2.inRange(hsv, lower, upper)
	img = cv2.erode(img, erosionKernel, iterations =1)
	img = cv2.dilate(img, dilateKernel, iterations=1)
	    # Blurring operation helps forthcoming findContours operation work better
	    # The values here can be adjusted to tune the detection quality.  (3,3) is a decent starting point
	img= cv2.blur(img, (3,3))
	    
	    # Find contours
	(_, cnts, _) = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    

	    # Sometimes the contours operation will find more than one contour
	    # But if we did all our preliminary operations properly, then the contour we need will be
	    # the *largest* contour in the set of all contours.  The sorted operation below sorts
	    # the cnts array of contours by area, so the first contour should be the largest
	  
	contours = sorted(cnts, key = cv2.contourArea, reverse = True)

	    # If no contours are detected, then don't try to process them or you'll get an error:
	if len(contours) > 0:
		cnt1 = contours[0]
		
		# Draw a minimum area rectangle around the contour
	rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
		
		# Draw the contour over image
	cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
	M1 = cv2.moments(cnt1)
	cx1 = int(M1['m10']/M1['m00'])
	cy1 = int(M1['m01']/M1['m00'])
	#draw center of cube on image in red
	cv2.circle(img,(cx1,cy1), 50, (0,0,255))
	#display center of image on img in white
	centX = int(width/2)
	centY = int(height/2)
	#error to be sent over network tables
	error = centX - cx1
	cv2.circle(img, (centX, centY),30, (255,255,255)) 
	cv2.imshow('frame', img)
	cv2.imshow('original', default)



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
