# Track a yellow cube and put a bounding box around it
# Currently, as of early Jan 2018, this is working on Mac MBP with its built-in camera
# From https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html#display-video
# press 'q' key to close video window when it's in the foreground

# SAVE:
# color notes jan 20:
# used pyimage utility with sliders to determine color range on video
# didn't have a cube with me.  used yellow climbing gym holds
# for yellow handles at climbing gym:
# H: 0-75
# S: 130-255
# V: 70-175


import numpy as np
import cv2

# Define the lower and upper boundaries of the color we need
# This is not easy to do, I'll try to explain some techniques in another document
lower = np.array([85,40,40])  # HSV
upper = np.array([97,200,255])

# A kernal is like a matrix that is used in the morphology operation
# See https://en.wikipedia.org/wiki/Kernel_(image_processing) if interested
# It's important to understand the basics of this operation so that you know
# what changing these values does.  These values should be experimented with
# to optimize detection.  Values like (4,4) are a reasonable starting point.
kernel = np.ones((6,6),np.uint8)

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    # cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Convert the image from RGB to HSV color space.  This is required for the next operation.
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Create a new image that contains yellow where the color was detected, otherwise purple? or black?
    img = cv2.inRange(img, lower, upper)

    # The morphological 'open' operation is described here:
    # https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
    # It helps remove noise and jagged edges, note how the stray speckles are removed!
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
   
    # Blurring operation helps forthcoming findContours operation work better
    # The values here can be adjusted to tune the detection quality.  (3,3) is a decent starting point
    img = cv2.blur(img, (3,3))
    
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
        
        # Draw the contour in red (255, 0, 0) on top of our original image
        cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
    
    cv2.imshow('frame', img)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


