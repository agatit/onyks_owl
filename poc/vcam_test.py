import cv2
import numpy as np
import math
from vcam.vcam import vcam,meshGen
import time

def nothing(x):
    pass

WINDOW_NAME = "ctrl"
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_NORMAL)
# cv2.resizeWindow(WINDOW_NAME,500,10)

# Creating the tracker bar for all the features
cv2.createTrackbar("X",WINDOW_NAME,500,1000,nothing)
cv2.createTrackbar("Y",WINDOW_NAME,500,1000,nothing)
cv2.createTrackbar("Z",WINDOW_NAME,0,1000,nothing)
cv2.createTrackbar("alpha",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("beta",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("gama",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("K1",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("K2",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("P1",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("P2",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("focus",WINDOW_NAME,40,1000,nothing)
cv2.createTrackbar("Sx",WINDOW_NAME,100,1000,nothing)
cv2.createTrackbar("Sy",WINDOW_NAME,100,1000,nothing)


scale = 2

#vid = cv2.VideoCapture("rtsp://admin:Kartofel_1410@192.168.1.44:554")
# vid = cv2.VideoCapture(0)
# ret, img = vid.read()
img = cv2.imread("resources/wagony_klatki/25_32.png")

H,W = img.shape[:2]
print(img.shape)
c1 = vcam(H=H,W=W)
plane = meshGen(H,W)
plane.Z = plane.X*0 + 1
pts3d = plane.getPlane()	

map_x,map_y = 0,0

def drawGrid(img, pxstep):
	x = pxstep
	y = pxstep
	#Draw all x lines
	while x < img.shape[1]:
		cv2.line(img, (x, 0), (x, img.shape[0]), color=(255, 0, 255), thickness=1)
		x += pxstep

	while y < img.shape[0]:
		cv2.line(img, (0, y), (img.shape[1], y), color=(255, 0, 255),thickness=1)
		y += pxstep

	return img


def update():
	global c1, map_x,map_y	

	X = -cv2.getTrackbarPos("X",WINDOW_NAME) + 500
	Y = -cv2.getTrackbarPos("Y",WINDOW_NAME) + 500
	Z = cv2.getTrackbarPos("Z",WINDOW_NAME)
	alpha = (cv2.getTrackbarPos("alpha",WINDOW_NAME) - 180) / 100
	beta = (cv2.getTrackbarPos("beta",WINDOW_NAME) - 180) / 50
	gamma = (cv2.getTrackbarPos("gama",WINDOW_NAME) - 180) / 100
	c1.focus = (cv2.getTrackbarPos("focus",WINDOW_NAME) - 500)/10
	c1.sx = (cv2.getTrackbarPos("Sx",WINDOW_NAME)+1)/100
	c1.sy = (cv2.getTrackbarPos("Sy",WINDOW_NAME)+1)/100
	k1 = (cv2.getTrackbarPos("K1",WINDOW_NAME)-50000)/100000000
	k2 = (cv2.getTrackbarPos("K2",WINDOW_NAME)-50000)/10000000000
	p1 = (cv2.getTrackbarPos("P1",WINDOW_NAME)-50000)/1000000
	p2 = (cv2.getTrackbarPos("P2",WINDOW_NAME)-50000)/1000000
	c1.KpCoeff[0] = k1
	c1.KpCoeff[1] = k2
	c1.KpCoeff[2] = p1
	c1.KpCoeff[3] = p2

	plane.Z = plane.X*0 + c1.focus # ?????
	pts3d = plane.getPlane()		

	c1.set_tvec(X,Y,Z)
	c1.set_rvec(alpha,beta,gamma)
	pts2d = c1.project(pts3d)
	map_x,map_y = c1.getMaps(pts2d)	

update()	

stime = time.time()

while True:
	# ret, img = vid.read()

	update()

	#img = c1.renderMesh(img)
	output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR)

	output = cv2.resize(output, (img.shape[1]//scale,img.shape[0]//scale))

	output = drawGrid(output, 20)

	cv2.imshow("output",output)
	cv2.waitKey(1)
	# key = cv2.waitKey(1) & 0xFF
	# if key == ord('q'):
	# 	break
	# elif key == ord(' '):
	# 	update()
