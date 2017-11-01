import cv2
import numpy as np

'''
Notes:

1- In image processing, a kernel, convolution matrix, or mask is a small matrix.
    a. Kernels are used for blurring, sharpening, embossing, edge detection, and more.
    b. This is accomplished by doing a convolution between a kernel and an image.

Reference:
http://docs.opencv.org/2.4/doc/tutorials/imgproc/gausian_median_blur_bilateral_filter/gausian_median_blur_bilateral_filter.html
'''

cap = cv2.VideoCapture(0)

while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # This is attempting to filter out all except the colour red
    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])
    mask = cv2.inRange(hsv, lower_red, upper_red)  # the colour filtered pixels (in white)
    res = cv2.bitwise_and(frame, frame, mask=mask)  # intersection between in the filtered pixels and the original frame

    cv2.imshow('Original', frame)
    cv2.imshow('res', res)

    # Blurs are caused by (computed by following an algorithm) Filters.
    # Filters main goal is to smooth an input image.
    # Blurs helps with noise, but clarity of the picture is lost: reduce image noise and reduce detail.
    # Some filters do not only dissolve the noise, but also smooth away the edges

    # One type of Blur is the "Averaging" method
    # kernels are necessary for "Averaging" method. Note the size and the divisor. This just suggests the size of an
    # area for applying the averaging.
    kernel = np.ones((15, 15), np.float32) / (15 * 15)
    smoothed = cv2.filter2D(res, -1, kernel)
    cv2.imshow('Averaging', smoothed)

    # Gaussian Blur: https://en.wikipedia.org/wiki/Gaussian_blur
    # is a low-pass filter, attenuating high frequency signals
    # is commonly used with edge detection
    blur = cv2.GaussianBlur(res, (15, 15), 0)
    cv2.imshow('Gaussian Blurring', blur)

    # Median Blur:
    # The median filter run through each element of the image and replace each pixel with the median of its neighboring
    # pixels (located in a square neighborhood around the evaluated pixel).
    median = cv2.medianBlur(res, 15)
    cv2.imshow('Median Blur', median)

    # Bilateral Blur:
    # This method attempts to reduce the noise, but also keep edge information.
    # http://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/MANDUCHI1/Bilateral_Filtering.html
    bilateral = cv2.bilateralFilter(res, 15, 75, 75)
    cv2.imshow('bilateral Blur', bilateral)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
