import numpy as np
import cv2

'''

References:
https://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
'''

img = cv2.imread('mainlogo.png')
gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
# gray = np.float32(gray)

corners = cv2.goodFeaturesToTrack(gray, 200, 0.001, 10)
corners = np.int16(corners)


for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 3, 255, -1)

while 1:
    cv2.imshow('Corner', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
