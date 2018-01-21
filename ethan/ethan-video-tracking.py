import numpy as np 
import cv2


#Changing colors to match green led ringlight
#Adding all the trackbars
#tracks yellow cube, put bounding box and display center
#doesn't start unless detecting cube
#press q to close video window

cap = cv.VideoCapture(0)

def nothing(x):
    pass

#setting up size of display 
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
cv2.namedWindow("detect", cv2.WINDOW_NORMAL)
cv2.resizeWindow("detect", 100,100)
cv2.namedWindow('HSVBars', cv2.WINDOW_NORMAL)
cv2.resizeWindow("detect", 100, 300)

#Kernel (google to see)

#Strings because I'm lazy
wnd = 'HSVBars'
lh = 'Lower Hue'
uh = 'Upper Hue'
ls = 'Lower Saturation'
us = 'Upper Saturation'
lv = 'Lower Value'
uv = 'Upper Value'

#Lower Trackbars
cv2.createTrackbar(lh, wnd, 0, 179, nothing)
cv2.createTrackbar(ls, wnd, 0, 255, nothing)
cv2.createTrackbar(lv, wnd, 0, 255, nothing)

#Upper Trackbars
cv2.createTrackbar(uh, wnd, 0, 179, nothing)
cv2.createTrackbar(us, wnd, 0, 255, nothing)
cv2.createTrackbar(uv, wnd, 0, 255, nothing)

while(True):

	#Reads Frame
	_, frame = cap read()

	#Converts from BGR to HSV
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	#Read trackbar changes
	lh = cv2.getTrackbarPos(hl, wnd)
	ls = cv2.getTrackbarPos(hh, wnd)
	lv = cv2.getTrackbarPos(sl, wnd)
	
	uh = cv2.getTrackbarPos(sh, wnd)
	us = cv2.getTrackbarPos(vl, wnd)
	uv = cv2.getTrackbarPos(vh, wnd)

	#Array for final values
	lower = np.array([lh, ls, lv])
	upper = np.array([uh, us, uv])

	#Creates mask for range
	mask = cv2.inRange(hsv, lower, upper)

	res = cv2.bitwise_and(frame, frame, mask = mask)

	#Kernel (Google to see)
	kernel = np.ones((31,31), np.uint8)

	#Gets rid of speckles
	closing = cv.morphologyEX(mask, cv.MORPH_OPEN, kernal)
	
	#Draw center of cube on image
	blur = cv2.blur(opened, (1,1))
	cv2.circle(blur,(cx1,cy1), 50, (0,100,100))
	cv2.imshow('detect', blur)
	    
# When everything done, release the capture
	cv2.imshow('frame', img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break		
cap.release()
cv2.destroyAllWindows()
