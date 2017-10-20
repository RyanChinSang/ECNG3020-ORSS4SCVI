import numpy as np
import cv2

# cap = cv2.VideoCapture('people-walking.mp4')
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while (1):
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