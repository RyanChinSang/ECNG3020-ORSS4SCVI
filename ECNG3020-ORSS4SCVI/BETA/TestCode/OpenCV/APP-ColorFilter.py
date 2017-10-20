import cv2
import numpy as np

'''
Blue  [[100:130], [100:255], [60:255]]
'''

def nothing(x):
    pass


cap = cv2.VideoCapture(0)

cv2.namedWindow('res')
cv2.createTrackbar('h1', 'res', 0, 180, nothing)
cv2.createTrackbar('s1', 'res', 0, 255, nothing)
cv2.createTrackbar('v1', 'res', 0, 255, nothing)
cv2.createTrackbar('h2', 'res', 180, 180, nothing)
cv2.createTrackbar('s2', 'res', 255, 255, nothing)
cv2.createTrackbar('v2', 'res', 255, 255, nothing)

while 1:
    _, frame = cap.read()
    # Change colour spaces; http://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('h1', 'res')
    s1 = cv2.getTrackbarPos('s1', 'res')
    v1 = cv2.getTrackbarPos('v1', 'res')
    h2 = cv2.getTrackbarPos('h2', 'res')
    s2 = cv2.getTrackbarPos('s2', 'res')
    v2 = cv2.getTrackbarPos('v2', 'res')

    # HSV - Hue, Saturation, Value
    # BGR - Blue, Green, Red
    lower_col = np.array([h1, s1, v1])
    upper_col = np.array([h2, s2, v2])

    mask = cv2.inRange(hsv, lower_col, upper_col)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
