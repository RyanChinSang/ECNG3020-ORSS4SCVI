import cv2

# Load 2 images of same size
img1 = cv2.imread('emmwat.jpg')
# img2 = cv2.imread('bradco.jpg')
img2 = cv2.imread('mainlogo.png')

# See #1.png
# add = img1+img2
# cv2.imshow('add', add)

# See #2.png
# (155,211,79) + (50, 170, 200) = 205, 381, 279...translated to (205, 255,255)
# add = cv2.add(img1, img2)
# cv2.imshow('add', add)

# See #3.png
# cv2.addWeighted(whichImg1, [weightofImg1], whichImg2, [weightofImg2], [gammaValue])
# add = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)
# cv2.imshow('add', add)

# I want to put logo on top-left corner, So I create a ROI
rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

# Now create a mask of logo and create its inverse mask
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# add a threshold - used to further simplify an image
# 220 <= mask <= 255
ret, mask = cv2.threshold(img2gray, 220, 255, cv2.THRESH_BINARY_INV)
mask_inv = cv2.bitwise_not(mask)

# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

dst = cv2.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

cv2.imshow('res', img1)             # See #4.png
cv2.imshow('mask_inv', mask_inv)    # See #5.png
cv2.imshow('img1_bg', img1_bg)      # See #6.png
cv2.imshow('img2_fg', img2_fg)      # See #7.png
cv2.imshow('dst', dst)              # See #8.png
cv2.waitKey(0)
cv2.destroyAllWindows()
