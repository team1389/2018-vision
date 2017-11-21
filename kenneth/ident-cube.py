import cv2 
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt



img = mpimg.imread("../cube.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
cv2.namedWindow("closed", cv2.WINDOW_NORMAL)
cv2.namedWindow("eroded", cv2.WINDOW_NORMAL)
cv2.namedWindow("opened", cv2.WINDOW_NORMAL)
cv2.resizeWindow("closed", 480, 360)
cv2.resizeWindow("eroded", 480, 360)
cv2.resizeWindow("opened", 480, 360)

# below values dont make sense, H is converted & makes sense, S&V don't make sense
#numbers only work if we use BGR2HSV
lower = np.array([15,90,90])  # HSV
upper = np.array([45,255,255])
res = cv2.inRange(hsv, lower, upper)

kernel = np.ones((11,11),np.uint8)

# The morphological 'open' operation is described here:
# https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
# It helps remove noise and jagged edges, note how the stray speckles are removed!
#TODO: Fuck around with this, to isolate our cube
#I'm thinking we close for full box, erode, then open for isolation, then dilate
#I don't think we need full box, given that we only need length + width
#having missing part doesn't matter that much
closed = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernel)
cv2.imshow("closed", closed)
eroded = cv2.erode(closed, kernel, iterations = 1)
cv2.imshow("eroded", eroded)

opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
cv2.imshow("opened", opened);

#TODO: find way to get center of the box, distance from each side
cv2.waitKey(0)
cv2.destroyAllWindows()
print('windows cleared')
