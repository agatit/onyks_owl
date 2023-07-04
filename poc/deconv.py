import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from scipy.signal import convolve2d as conv2

from skimage import color, io, restoration

title_window = "deconv"

img = color.rgb2gray(io.imread('25_32.png'))
img = img[355:470, 1301:1450]

show_zoom = 8
kernel_len = 15
kernel_line = np.zeros((kernel_len), np.float32)

def on_trackbar(val, index):
    global kernel_line

    kernel_line[index] = val / 10
    kernel_line[kernel_len-index-1] = val / 10    
    kernel = kernel_line / np.sum(kernel_line)

    psf = np.zeros((kernel_len, kernel_len), np.float32)
    psf[kernel_len//2:kernel_len//2+1,:] = kernel[:]

    print(np.array2string(kernel, precision=2)) 

    # img_deconv = restoration.richardson_lucy(img, psf, num_iter=10)
    img_deconv = restoration.wiener(img, psf, 0.05)

    cv.imshow(title_window, cv.resize(img_deconv, np.array(np.shape(img_deconv))*show_zoom))
    # cv.imshow("psf", cv.resize(psf, np.array(np.shape(psf))*8))
    print(np.array2string(psf[kernel_len//2,:], precision=2)) 

def get_on_trackbar(index):
    return lambda v: on_trackbar(v, index)


cv.imshow(title_window, cv.resize(img, np.array(np.shape(img))*show_zoom))

for i,v in enumerate(kernel_line[0:kernel_len//2+1]):
    cv.createTrackbar(f"{i}", title_window, 10, 100, get_on_trackbar(i))
# cv.createTrackbar(f"długosc", title_window, 10, 100, on_trackbar_len)

on_trackbar(kernel_line[0],0)
cv.waitKey()