import cv2

cap = cv2.VideoCapture(0)
'''
Notes:

1- Most edge-detection algorithms are sensitive to noise.

2- The Canny Edge Detection algorithm is as follows:
    a. Noise Reduction using a 5x5 Gaussian filter.
    b. Find Intensity Gradient magnitude and angle.
        i. Filtered with Sobel kernel in both x and y directions (done separately) to get:
            a. Intensity Gradient in x (horizontal) direction, Gx
            b. Intensity Gradient in y (vertical) direction, Gy
       ii. Compute the Gradient (Edge) Magnitude: Gm = sqrt( (Gx)^2 + (Gy)^2 )
      iii. Compute the Gradient Direction (Angle): Ga = arctan( Gy / Gx )
            a. Gradient direction is always perpendicular to edges.
            b. Rounded to one of Four (4) angles:
                1. Horizontal      [-]: 0' or 180' or 360'
                2. Diagonal x+y    [/]: 45' or 225'
                3. Vertical        [|]: 90' or 270'
                4. Diagonal -(x+y) [\]: 135' or 315'
    c. Non-Maximum Suppression: Scan to remove any unwanted pixels which may not constitute the edge.
        i. At every pixel, the pixel is checked if it is a local maximum in its neighbourhood in the direction Ga.
           i.e. Pixels A, B and C in the direction Ga are checked to find which is the local maximum.
                The intensity of points A->B, B->C and C->A are compared.
       ii. The resulting pixel that is a local maximum is subject to Hysteresis Thresholding.
      iii. All other pixels (not the local maximum) is suppressed (put to zero).
    d. Hysteresis Thresholding: Decides if all detected local maximums are really edges, or not.
        i. Two threshold values minVal and maxVal are defined:
            a. For any local maximum:
                1. Above maxVal: is considered a "sure-edge"
                2. Below minVal: is discarded (put to zero)
                3. Between minVal and maxVal: are considered based on its connectivity
                    a. If connected to a "sure-edge", the value is kept
                    b. Else, is discarded (put to zero)
       ii. Remove small pixel noises on the assumption that edges are lines.
    This algorithm returns only the "strong edges".

References:
\TUT-EdgeDet\Canny Edge Detection - OpenCV.pdf
'''
while 1:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('Original', frame)
    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow('Edges', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
