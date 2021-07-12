from __future__ import print_function
from __future__ import division
import cv2 as cv
import argparse
import os

alpha_slider_max = 100
title_window = 'Linear Blend'

def on_trackbar(val):
    alpha = val / alpha_slider_max
    beta = ( 1.0 - alpha )
    dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
    cv.imshow(title_window, dst)

parser = argparse.ArgumentParser(description='Code for Adding a Trackbar to our applications tutorial.')
parser.add_argument('--input1', help='Path to the first input image.', default=os.path.join(os.path.abspath(os.path.dirname(__file__)),'./Linuxlogo.jpg'))
parser.add_argument('--input2', help='Path to the second input image.', default=os.path.join(os.path.abspath(os.path.dirname(__file__)),'./Windowslogo.jpg'))
args = parser.parse_args()

src1 = cv.imread(args.input1)
src1 = cv.resize(src1, (640, 480))
src2 = cv.imread(args.input2)
src2 = cv.resize(src2, (640, 480))

if src1 is None:
    print('Could not open or find the image: ', args.input1)
    exit(0)

if src2 is None:
    print('Could not open or find the image: ', args.input2)
    exit(0)

cv.namedWindow(title_window)
trackbar_name = 'Alpha x %d' % alpha_slider_max
cv.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)

# Show some stuff
on_trackbar(0)
# Wait until user press some key
cv.waitKey()