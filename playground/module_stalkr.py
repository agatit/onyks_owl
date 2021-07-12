import cv2
import numpy as np

import os

# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../samples/youtube/out_2_15.mp4')
path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para_01.jpg')
path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para_02.jpg')
path3 = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para_03.jpg')

# # v_name = './../samples/youtube/out_2_15.mp4' #Nazwa pliku
# cap = cv2.VideoCapture(v_name) #Tworzenie obiektu obrazu
# ret, img = cap.read() #Pobieranie obrazu z pliku
# while ret:
#     cv2.imshow('image', img)
#     ret, img = cap.read()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#Zakończenie działania programu

image1 = cv2.imread(path1,0)
image2 = cv2.imread(path2,0)
image3 = cv2.imread(path3)

image1m = cv2.resize(image1, (int(image1.shape[1]/4), int(image1.shape[0]/4)))
image2m = cv2.resize(image2, (int(image1.shape[1]/4), int(image2.shape[0]/4)))
image3m = cv2.resize(image1, (int(image3.shape[1]/4), int(image3.shape[0]/4)))

# cv2.imshow('image1', image1m)
# cv2.imshow('image2', image2m)
# cv2.imshow('image3', image3m)

# stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
# disparity = stereo.compute(image1m,image2m)
# cv2.imshow('disparity',disparity)
# cv2.show()

# image1s = cv2.stereoRectify()
cv2.waitKey(0)
# cap.release()
cv2.destroyAllWindows()



R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(  cameraMatrix1,
                                                                    distCoeffs1,
                                                                    cameraMatrix2,
                                                                    distCoeffs2,
                                                                    imageSize,
                                                                    # R,
                                                                    # T[,
                                                                    # R1[,
                                                                    # R2[,
                                                                    # P1[,
                                                                    # P2[,
                                                                    # Q[,
                                                                    # flags[,
                                                                    # alpha[,
                                                                    # newImageSize
                                                                    # ]]]]]]]]	
                                                                    )