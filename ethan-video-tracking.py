import numpy as np
import cv2
#Still untested with live video on both computer and ps eye
#working with video from phone
#track yellow cube, put bounding box and display center
#press q to close video window


#setting up size of display 
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
cv2.namedWindow("detect", cv2.WINDOW_NORMAL)
cv2.resizeWindow("detect", 100,100)

lower = np.array([85,40,40])  # HSV
upper = np.array([100,200,280])

kernel = np.ones((31,31), np.uint8)

cap = cv2.VideoCapture(0)

while(True):
	#setting up size of display window 
	#reading every frame
	ret, img = cap.read()
	cv2.imshow('frame', img)
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
	hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	    # Create a new image that contains yellow where the color was detected, otherwise purple? or black?
	res = cv2.inRange(hsv, lower, upper)

	    # The morphological 'open' operation is described here:
	    # https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
	    # It helps remove noise and jagged edges, note how the stray speckles are removed!
	opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
	   
	    # Blurring operation helps forthcoming findContours operation work better
	    # The values here can be adjusted to tune the detection quality.  (3,3) is a decent starting point
	blur = cv2.blur(opened, (1,1))
	    
	    # Find contours
	(_, cnts, _) = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    

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
	cv2.drawContours(blur, [rect1], -1, (255, 0, 0), 2)
	M1 = cv2.moments(cnt1)
	cx1 = int(M1['m10']/M1['m00'])
	cy1 = int(M1['m01']/M1['m00'])
	#draw center of cube on image
	cv2.circle(blur,(cx1,cy1), 50, (0,100,100))
	cv2.imshow('detect', blur)

using namespace cv;

# Global Variables
const int hue_slider_max = 255;
int hue_slider;
double hue
const int saturation_slider_max = 255;
int saturation_slider;
double saturation
const int value_slider_max = 255;
int value_slider;


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()