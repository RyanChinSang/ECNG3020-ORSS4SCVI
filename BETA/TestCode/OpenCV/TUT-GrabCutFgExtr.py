import cv2
import numpy as np
import matplotlib.pyplot as plt

'''

Starting with a user-specified bounding box (the box with the smallest measure within which all the points lie) around 
the object to be segmented, the algorithm estimates the color distribution of the target object and that of the 
background using a Gaussian mixture model (a probabilistic model for representing the presence of sub-populations within 
an overall population). 

This is used to construct a Markov random field (a set of random variables whose future states depend only upon the 
current state) over the pixel labels, with an energy function (mathematical optimization) that prefers connected 
regions having the same label, and running a graph cut based optimization to infer their values. 

As this estimate is likely to be more accurate than the original, taken from the bounding box, this two-step procedure 
is repeated until convergence.

'''

img = cv2.imread('bradco.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (0, 0, 300, 300)

cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]

plt.imshow(img)
plt.colorbar()
plt.show()
