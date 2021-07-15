from skimage import  io,img_as_ubyte,img_as_float
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
from skimage.segmentation import random_walker
from skimage.morphology import opening,disk
import os
import cv2
import time

# Read image
img_full = img_as_float(io.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_full.png')))
img_disp = img_as_float(io.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_disp.png')))
gray_img = rgb2gray(img_full)
h,w = gray_img.shape
 

 
# Random walk segmentation
markers = img_disp # np.zeros_like(gray_img)
markers[markers!= 0] = 1
# markers[markers>1] = 1
markers = rgb2gray(markers)
# markers[gray_img>0.8]=1
# markers[gray_img<0.45]=2

# Results obtained using random walk algorithm
start_time = time.time()
labels = random_walker(gray_img,markers,beta=10,mode="bf")
print("--- %s seconds ---" % (time.time() - start_time))
# plt.imshow(labels)
 
 # Convert to boolean
segm1 = (labels>1.1)
# print(segm1)
 
 # Morphology open operation

kernel = disk(10)   
img_opening = opening(segm1,kernel)
 
 # Convert single channel threshold to RGB channel threshold
segm = np.tile(img_opening.reshape(h,w,1),3)
# print(segm)
 
 # Copy color image
rgb_img = img_full.copy()
 # Mask operation
rgb_img[segm] = 0
 
#  # Display image
# plt.figure(figsize=(10,8),dpi=80)
# plt.subplot(121)
# plt.imshow(img_full)
# plt.xlabel("Original image",fontproperties='SimHei')
# plt.subplot(122)
# plt.imshow(rgb_img)
# plt.xlabel("Segmentation result", fontproperties='SimHei')
# # plt.subplot(122)
# # plt.imshow(markers)
# # plt.xlabel("Markers", fontproperties='SimHei')
# plt.show()

final = cv2.normalize(rgb_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
finale = cv2.cvtColor(final, cv2.COLOR_RGB2BGR)
cv2.imwrite(os.path.join(os.path.abspath(os.path.dirname(__file__)),'./test_rw.png'), finale)