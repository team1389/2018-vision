import numpy as np
import cv2
img = cv2.imread('./cube.jpg')

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

cv2.resizeWindow("frame", 900,900)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 900,900)



	
erosionKernel = np.ones((3,3), np.uint8)
dilateKernel = np.ones((3,3), np.uint8)

lower = np.array([15,125,125])  # HSV

	#increased upper HSV vals	

upper = np.array([40,255,255])
default = img;
		    # Display the resulting frame
		    # cv2.imshow('frame', img)

		    # Convert the image from RGB to HSV color space.  This is required for the next operation.
#note that opencv uses BGR
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		    # Create a new image that contains yellow where the color was detected, otherwise purple? or black?
img = cv2.inRange(hsv, lower, upper)

	  
	    # Try an Erosion here for noise/speckle reduction
	#img = cv2.erode(img, erosionKernel, iterations = 1)

	    # Try a Dilation operation here to re-group the object(s)
	#img = cv2.dilate(img, dilateKernel, iterations = 1)
		   
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
#rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
		
		# Draw the contour over image
#cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
#M1 = cv2.moments(cnt1)
#cx1 = int(M1['m10']/M1['m00'])
#cy1 = int(M1['m01']/M1['m00'])
#draw center of cube on image
#cv2.circle(img,(cx1,cy1), 50, (0,100,100))
cv2.imshow('frame', img)
cv2.imshow('original', default)

cv2.waitKey(0)
