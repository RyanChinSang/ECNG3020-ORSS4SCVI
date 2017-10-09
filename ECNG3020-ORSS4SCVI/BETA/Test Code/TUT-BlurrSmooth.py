import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])

    mask = cv2.inRange(hsv, lower_red, upper_red)  # the colour filtered pixels (in white)
    res = cv2.bitwise_and(frame, frame, mask=mask)  # intersection between in the filtered pixels and the original frame

    cv2.imshow('Original', frame)
    cv2.imshow('res', res)

    # Blurs helps with noise, but clarity of the picture is lost: reduce image noise and reduce detail
    # For a Blur, you can use the "Averaging" method
    # kernels are necessary for "Averaging" method. Note the size and the divisor. This just suggests the size of an
    #   area for applying the averaging.
    kernel = np.ones((15, 15), np.float32) / (15 * 15)
    smoothed = cv2.filter2D(res, -1, kernel)  #
    cv2.imshow('Averaging', smoothed)

    # Gaussian Blur: https://en.wikipedia.org/wiki/Gaussian_blur
    # is a low-pass filter, attenuating high frequency signals
    # is commonly used with edge detection

    blur = cv2.GaussianBlur(res, (15, 15), 0)
    cv2.imshow('Gaussian Blurring', blur)

    # Median Blur:
    median = cv2.medianBlur(res, 15)
    cv2.imshow('Median Blur', median)

    # Bilateral Blur:
    bilateral = cv2.bilateralFilter(res, 15, 75, 75)
    cv2.imshow('bilateral Blur', bilateral)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
