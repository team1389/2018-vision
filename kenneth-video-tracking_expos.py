import numpy as np
import cv2
import os
#Still untested with live video on both computer and ps eye
#working with video from phone
#track yellow cube, put bounding box and display center
#press q to close video window

os.system('v4l2-ctl -c exposure=120')
os.system('v4l2-ctl -c contrast=10')
#setting up size of display 
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 100,100)
	
#erosionKernel = np.ones((15,15), np.uint8)
#dilateKernel = np.ones((7,7), np.uint8)
erosionKernel = np.ones((21,21), np.uint8)
dilateKernel = np.ones((3,3), np.uint8)
#as we raise S value, we stop registering brighter shades
#determine how important seeing said brighter shades
#at current vals, unable to see side being illuminated from most angles
lower = np.array([23,140,76])  # HSV
upper = np.array([35,255,140])


cap = cv2.VideoCapture(0)
os.system('v4l2-ctl -c exposure=10')
while(True):
	#setting up size of display window 
	#reading every frame
	ret, img = cap.read()
	default = img
	#lower = np.array([lH,lS,lV])
	#upper = np.array([hH,hS,hV])
	#increased upper HSV vals	
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
	    # Our operations on the frame come here
	    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	    # Display the resulting frame
	    # cv2.imshow('frame', img)

	    # Convert the image from RGB to HSV color space.  This is required for the next operation.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
		rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
		
		# Draw the contour over image
		cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
		M1 = cv2.moments(cnt1)
		cx1 = int(M1['m10']/M1['m00'])
		cy1 = int(M1['m01']/M1['m00'])
	#draw center of cube on image
		cv2.circle(img,(cx1,cy1), 50, (0,100,100))
	cv2.imshow('frame', img)
	cv2.imshow('original', default)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
