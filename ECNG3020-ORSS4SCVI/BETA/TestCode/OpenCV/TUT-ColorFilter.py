import cv2
import numpy as np

# USE:
# a to increase lower_col[0]
# z to decrease lower_col[0]
# s to increase upper_col[0]
# x to decrease upper_col[0]

# d to increase lower_col[1]
# c to decrease lower_col[1]
# f to increase upper_col[1]
# v to decrease upper_col[1]

# g to increase lower_col[2]
# b to decrease lower_col[2]
# h to increase upper_col[2]
# n to decrease upper_col[2]


cap = cv2.VideoCapture(0)
a = 0
d = 0
g = 0
s = 255
f = 255
h = 255


while 1:
    _, frame = cap.read()
    # Change colour spaces; http://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV - Hue, Saturation, Value
    # BGR - Blue, Green, Red
    lower_col = np.array([a, d, g])
    upper_col = np.array([s, f, h])

    mask = cv2.inRange(hsv, lower_col, upper_col)
    # mask = cv2.inRange(frame, lower_col, upper_col)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('a'):
        a = a + 5
    elif cv2.waitKey(1) & 0xFF == ord('z'):
        a = a - 5
    if cv2.waitKey(1) & 0xFF == ord('s'):
        s = s + 5
    elif cv2.waitKey(1) & 0xFF == ord('x'):
        s = s - 5

    if cv2.waitKey(1) & 0xFF == ord('d'):
        d = d + 5
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        d = d - 5
    if cv2.waitKey(1) & 0xFF == ord('f'):
        f = f + 5
    elif cv2.waitKey(1) & 0xFF == ord('v'):
        f = f - 5

    if cv2.waitKey(1) & 0xFF == ord('g'):
        g = g + 5
    elif cv2.waitKey(1) & 0xFF == ord('b'):
        g = g - 5
    if cv2.waitKey(1) & 0xFF == ord('h'):
        h = h + 5
    elif cv2.waitKey(1) & 0xFF == ord('n'):
        h = h - 5

    if cv2.waitKey(1) & 0xFF == ord('i'):
        a = 0
    elif cv2.waitKey(1) & 0xFF == ord('I'):
        a = 255
    if cv2.waitKey(1) & 0xFF == ord('o'):
        d = 0
    elif cv2.waitKey(1) & 0xFF == ord('O'):
        d = 255
    if cv2.waitKey(1) & 0xFF == ord('p'):
        g = 0
    elif cv2.waitKey(1) & 0xFF == ord('P'):
        g = 255

    if cv2.waitKey(1) & 0xFF == ord('k'):
        s = 0
    elif cv2.waitKey(1) & 0xFF == ord('K'):
        s = 255
    if cv2.waitKey(1) & 0xFF == ord('l'):
        f = 0
    elif cv2.waitKey(1) & 0xFF == ord('L'):
        f = 255
    if cv2.waitKey(1) & 0xFF == ord(';'):
        h = 0
    elif cv2.waitKey(1) & 0xFF == ord(':'):
        h = 255

    if cv2.waitKey(1):
        print("a = [" + str(a) + ", " + str(s) + "], " +
              "d = [" + str(d) + ", " + str(f) + "], " +
              "g = [" + str(g) + ", " + str(h) + "]")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
