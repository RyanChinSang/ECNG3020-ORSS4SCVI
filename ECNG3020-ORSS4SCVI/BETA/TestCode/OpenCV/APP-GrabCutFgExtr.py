import cv2
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass

cv2.namedWindow('res')
cv2.createTrackbar('a1', 'res', 0, 500, nothing)
cv2.createTrackbar('a2', 'res', 0, 500, nothing)
cv2.createTrackbar('b1', 'res', 565, 565, nothing)
cv2.createTrackbar('b2', 'res', 565, 565, nothing)

img = cv2.imread('emmwat.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)


while 1:
    a1 = cv2.getTrackbarPos('a1', 'res')
    a2 = cv2.getTrackbarPos('a2', 'res')
    b1 = cv2.getTrackbarPos('b1', 'res')
    b2 = cv2.getTrackbarPos('b2', 'res')
    rect = (a1, a2, b1, b2)

    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]

    cv2.imshow('res', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#
# plt.imshow(img)
# plt.colorbar()
# plt.show()
