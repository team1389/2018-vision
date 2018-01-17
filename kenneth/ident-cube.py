import cv2 
import numpy as np
import matplotlib.image as mpimg

from matplotlib import pyplot as plt







img = mpimg.imread("../cube.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 900,900)

# below values dont make sense, H is converted & makes sense, S&V don't make sense
#numbers only work if we use BGR2HSV
lower = np.array([15,90,90])  # HSV
upper = np.array([45,255,255])
res = cv2.inRange(hsv, lower, upper)


kernel = np.ones((9,9),np.uint8)



#tune iterations and kernal size

eroded = cv2.erode(res, kernel, iterations = 6)

(_, cnts, _) = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Sometimes the contours operation will find more than two contours
# But if we did all our preliminary operations properly, then the two contours we need will be
# the *largest* contours in the set of contours.  The sorted operation below sorts
# the cnts array of contours by area, so the first two contours will be the largest

cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
cnt2 = sorted(cnts, key = cv2.contourArea, reverse = True)[1]

rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
rect2 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt2)))
# Draw the contours in red (255, 0, 0) on top of our original image
cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
cv2.drawContours(img, [rect2], -1, (255, 0, 0), 2)

# Get the moment of the contour: https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html
# it's like the center
M1 = cv2.moments(cnt1)
cx1 = int(M1['m10']/M1['m00'])
cy1 = int(M1['m01']/M1['m00'])
cv2.circle(img,(cx1,cy1), 5, (0,0,255), -1)
M2 = cv2.moments(cnt2)
cx2 = int(M2['m10']/M2['m00'])
cy2 = int(M2['m01']/M2['m00'])
cv2.circle(img,(cx2,cy2), 5, (0,0,255), -1)

# Next steps: find the center point between the two pieces of tape
center = (round((cx1 + cx2)/2), round((cy1 + cy2)/2))
cv2.circle(img, center, 5, (255,0,0), -1)
height, width, channels = img.shape
img_center = (width, height)
cv2.imshow("image", img)


#TODO: find way to get center of the box, distance from each side
cv2.waitKey(0)
cv2.destroyAllWindows()
print('windows cleared')
