import cv2

'''
Notes:
    
1- cv2.CV_64F is a higher precision datatype that would prevent data loss on White-to-Black transitions (-ve slopes)
   seen on the cv2.CV_8U datatype, which converts -ves into 0s. Therefore, edges are not lost using cv2.CV_64F.

References:
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_gradients/py_gradients.html?highlight=cv2%20cv_64f
'''

cap = cv2.VideoCapture(0)

while 1:
    _, frame = cap.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Original', frame)

    # It calculates the Laplacian of the image where each derivative is found using Sobel derivatives.
    # The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated
    # using the Sobel operator.
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    cv2.imshow('laplacian', laplacian)

    # ksize is the kernel size
    # Sobel operators is a joint Gausssian smoothing plus differentiation operation, so it is more resistant to noise.
    # ~~x - apply the ~~ operation in the horizontal direction
    # ~~y - apply the ~~ operation in the vertical direction
    # ~~xy - apply the ~~ operation in both vertical and horizontal direction
    # Scharr gives better results than Sobel.

    # sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    # cv2.imshow('sobelx', sobelx)
    # scharrx = cv2.Scharr(frame, cv2.CV_64F, 1, 0)
    # cv2.imshow('scharrx', scharrx)

    # sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
    # cv2.imshow('sobely', sobely)
    # scharry = cv2.Scharr(frame, cv2.CV_64F, 0, 1)
    # cv2.imshow('scharry', scharry)

    # When ksize=1 here, it is approximately the laplacian (like a dilated laplacian)
    sobelxy = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5)
    cv2.imshow('sobelxy', sobelxy)
    # Cannot get Scharrxy, why?
    # error: (-215) dx >= 0 && dy >= 0 && dx+dy == 1 in function cv::getScharrKernels
    # scharrxy = cv2.Scharr(frame, cv2.CV_64F, 1, 1)
    # cv2.imshow('scharrxy', scharrxy)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
