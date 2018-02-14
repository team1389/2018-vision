import numpy as np
import cv2
import os
#meant to take picture with same settings as current vid-tracking code
#to go over in gimp
cap = cv2.VideoCapture(0)
#exposure at default, contrast down from 32
os.system('v4l2-ctl -c brightness=0')
os.system('v4l2-ctl -c contrast=32')
os.system('v4l2-ctl -c gain=20')

#kernel size is different
erosionKernel = np.ones((1,1), np.uint8)
dilateKernel = np.ones((1,1), np.uint8)
lower = np.array([15,25,153])  # HSV
#V was 127
upper = np.array([100,102,204])
ret, img = cap.read()
cv2.imwrite('./pic.jpg', img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img = cv2.inRange(hsv, lower, upper)
img = cv2.erode(img, erosionKernel, iterations =1)
img = cv2.dilate(img, dilateKernel, iterations=1)
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
	#draw center of cube on image
    cv2.circle(img,(cx1,cy1), 50, (0,100,100))
cv2.imwrite('./maskedpic.jpg', img)
