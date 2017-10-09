import cv2
import numpy as np

cap = cv2.VideoCapture(0)
'''
Notes:

1- Most edge-detection algorithms are sensitive to noise;


'''
while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_col = np.array([30, 150, 50])
    upper_col = np.array([255, 255, 180])

    mask = cv2.inRange(hsv, lower_col, upper_col)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original', frame)
    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow('Edges', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
