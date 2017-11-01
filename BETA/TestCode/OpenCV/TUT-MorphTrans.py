import cv2
import numpy as np

# References:
# https://docs.opencv.org/2.4/doc/tutorials/imgproc/opening_closing_hats/opening_closing_hats.html?highlight=opening

cap = cv2.VideoCapture(0)

while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # This is attempting to filter out all except the colour red/maroon
    lower_red = np.array([130, 100, 0], np.uint8)
    upper_red = np.array([255, 255, 255], np.uint8)
    mask = cv2.inRange(hsv, lower_red, upper_red)  # the colour filtered pixels (in white)
    res = cv2.bitwise_and(frame, frame, mask=mask)  # intersection between in the filtered pixels and the original frame

    # Morphological Operations
    # A set of operations that process images based on shapes.
    # Morphological operations apply a structuring element to an input image and generate an output image.
    # 1 - Removes noise
    # 2 - Isolation of individual elements and joining disparate elements in an image.
    # 3 - Finding of intensity bumps or holes in an image.

    kernel = np.ones((5, 5), np.uint8)
    # Dilation
    # Convolves an image A with some kernel (B), which can have any shape or size, usually a square or circle.
    # The kernel B has a defined anchor point, usually being the center of the kernel.
    # Scan the kernel B over the image.
    # Compute the maximal pixel value overlapped by B.
    # Replace the image pixel in the anchor position with the maximal value.
    # This causes the bright regions in the image to "grow" - makes the object bigger.
    dilation = cv2.dilate(mask, kernel, iterations=1)
    cv2.imshow('dilation', dilation)

    # Erosion
    # This computes a local minimum over the area of the kernel B.
    # Replace the image pixel in the anchor position with the minimal value.
    # This causes the bright regions in the image to "shrink" - makes the object smaller.
    # NOTE: Taking the erosion of the dilation with the same kernel size returns the original input.
    erosion = cv2.erode(mask, kernel, iterations=1)
    cv2.imshow('erosion', erosion)

    # Opening
    # Is obtained by the erosion of an image followed by a dilation.
    # Useful for removing small objects (it is assumed that the objects are bright on a dark foreground)
    # Removes "false positives".
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    cv2.imshow('Opening', opening)

    # Closing
    # Is obtained by the dilation of an image followed by an erosion.
    # Useful to remove small holes (dark regions).
    # Removes "false negatives".
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('Closing', closing)

    # Morphological Gradient
    # It is the difference between the dilation and the erosion of an image.
    # It is useful for finding the outline of an object
    mgrad = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
    cv2.imshow('mgrad', mgrad)

    # It is the difference between input image and Opening of the image
    tophat = cv2.morphologyEx(mask, cv2.MORPH_TOPHAT, kernel)
    cv2.imshow('Tophat', tophat)

    # It is the difference between the closing of the input image and input image.
    blackhat = cv2.morphologyEx(mask, cv2.MORPH_BLACKHAT, kernel)
    cv2.imshow('Blackhat', blackhat)

    cv2.imshow('Original', frame)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
