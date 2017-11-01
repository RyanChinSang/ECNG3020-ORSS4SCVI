import numpy as np
import cv2


def copypaste(start, vsize, hsize, dest):
    reg = img[start[0]:(start[0] + vsize), start[1]:(start[1] + hsize)]
    img[dest[0]:(dest[0] + vsize), dest[1]:(dest[1] + hsize)] = reg


def cutpaste(start, vsize, hsize, dest):
    copypaste(start, vsize, hsize, dest)
    img[start[0]:(start[0] + vsize), start[1]:(start[1] + hsize)] = [255, 255, 255]


img = cv2.imread('doorway.jpg', cv2.IMREAD_COLOR)

# More drawing: http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
# Draw a line (onWhich, whereStart, whereEnd, colour, lineWidth)
cv2.line(img, (0, 0), (200, 300), (255, 255, 255), 50)
# Draw a rectangle (onWhich, whereStart, whereEnd, colour, lineWidth)
cv2.rectangle(img, (500, 250), (1000, 500), (0, 0, 255), 15)
# Draw a circle (onWhich, whereCentre, radius, colour, lineWidth)
cv2.circle(img, (447, 63), 63, (0, 255, 0), -1)  # -1 lw is a filled-in shape

# Draw a polygon (onWhich, wherePts, isClosed?, colour, lineWidth)
pts = np.array([[100, 50], [200, 300], [700, 200], [500, 100]], np.int32)  # Points for the edges of the polygon
# pts = pts.reshape((-1, 1, 2))  # Might not be necessary
cv2.polylines(img, [pts], True, (0, 255, 255), 0)
# NB: "True" here means if the polygon is closed, or not/False.
# NB2: lw=0 defaults the lw to 1 anyway

# Select a font to use for texts; http://www.codesofinterest.com/2017/07/more-fonts-on-opencv.html
font = qq
# Draw text (onWhich, whatText, whereStart, whichFont, fontScale, fontColor, fontThickness, AntiAliasing)
cv2.putText(img, 'OpenCV Tuts!', (10, 500), font, 6, (200, 255, 155), 13, cv2.LINE_AA)

roi = img[37:111, 107:194]
img[0:74, 0:87] = roi
# copypaste((37, 107), 74, 87, (0, 0))
# cutpaste((37, 107), 74, 87, (0, 0))

# Useful img properties
print(img.shape)  # (verticalPx], [horizontalPx], [#ColourCh])
print(img.size)   # img.size = [verticalPx]*[horizontalPx]*[#ColourCh]
print(img.dtype)  # data type = uint8 i.e. unsigned 8-bit integer

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
