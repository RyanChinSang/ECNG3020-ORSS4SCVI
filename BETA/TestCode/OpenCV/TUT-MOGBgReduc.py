import numpy as np
import cv2

# cap = cv2.VideoCapture('people-walking.mp4')
'''
It is also a Gaussian Mixture-based Background/Foreground Segmentation Algorithm. It is based on two papers by 
Z.Zivkovic, "Improved adaptive Gausian mixture model for background subtraction" in 2004 and "Efficient Adaptive Density
Estimation per Image Pixel for the Task of Background Subtraction" in 2006. One important feature of this algorithm is 
that it selects the appropriate number of gaussian distribution for each pixel. (Remember, in last case, we took a K 
gaussian distributions throughout the algorithm). It provides better adaptibility to varying scenes due illumination 
changes etc.

REF:
https://docs.opencv.org/3.3.0/db/d5c/tutorial_py_bg_subtraction.html
'''

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while 1:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    # fgmask3 = np.repeat(fgmask[:, :, np.newaxis], 3, axis=2)
    # red = (frame - fgmask3)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)

    cv2.imshow('frame', frame)
    cv2.imshow('fgmask', fgmask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()