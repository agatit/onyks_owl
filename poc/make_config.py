import cv2
import numpy as np
import math
import argparse
import json

import rectify

def nothing(x):
    pass

parser = argparse.ArgumentParser()
parser.add_argument("image_file")
parser.add_argument("config_file")
parser.add_argument("--scale", type=int, default=2)
args = parser.parse_args()

WINDOW_NAME = "ctrl"
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_NORMAL)

config = {}

view_scale = args.scale
img = cv2.imread(args.image_file)
H,W = img.shape[:2]


# Creating the tracker bar for all the features
cv2.createTrackbar("X",WINDOW_NAME,W//2,2*W,nothing)
cv2.createTrackbar("Y",WINDOW_NAME,H//2,2*H,nothing)
cv2.createTrackbar("scale",WINDOW_NAME,50,100,nothing)
cv2.createTrackbar("alpha",WINDOW_NAME,90,180,nothing)
cv2.createTrackbar("beta",WINDOW_NAME,90,180,nothing)
cv2.createTrackbar("gama",WINDOW_NAME,90,180,nothing)
cv2.createTrackbar("K1",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("K2",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("P1",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("P2",WINDOW_NAME,50000,100000,nothing)
cv2.createTrackbar("focus",WINDOW_NAME,40,300,nothing)


def drawGrid(img, pxstep):
    x = pxstep
    y = pxstep
    #Draw all x lines
    while x < img.shape[1]:
        cv2.line(img, (x, 0), (x, img.shape[0]), color=(180, 0, 0), thickness=1)
        x += pxstep

    while y < img.shape[0]:
        cv2.line(img, (0, y), (img.shape[1], y), color=(180, 0, 0),thickness=1)
        y += pxstep

    return img


def get_config():
    config = {}

    config['sensor_h'] = 3.69 #mm # 1/3″
    config['sensor_w'] = 7.38 #mm
    config['X'] = cv2.getTrackbarPos("X",WINDOW_NAME) - W//2  # pixels
    config['Y'] = cv2.getTrackbarPos("Y",WINDOW_NAME) - H//2
    config['scale'] = cv2.getTrackbarPos("scale",WINDOW_NAME) / 50 # pixels
    config['alpha'] = math.radians( (cv2.getTrackbarPos("alpha",WINDOW_NAME) - 90) ) # radians
    config['beta'] = math.radians( (cv2.getTrackbarPos("beta",WINDOW_NAME) - 90) )
    config['gamma'] = math.radians( (cv2.getTrackbarPos("gama",WINDOW_NAME) - 90) )
    config['focus'] = cv2.getTrackbarPos("focus",WINDOW_NAME)/10 # milimeters
    k1 = (cv2.getTrackbarPos("K1",WINDOW_NAME)-50000)/100000
    k2 = (cv2.getTrackbarPos("K2",WINDOW_NAME)-50000)/1000000
    p1 = (cv2.getTrackbarPos("P1",WINDOW_NAME)-50000)/1000000
    p2 = (cv2.getTrackbarPos("P2",WINDOW_NAME)-50000)/1000000
    config['dist'] = [k1, k2, p1, p2]

    return config    


def drawSrcGrid(img, pxstep):
    scale = cv2.getTrackbarPos("scale",WINDOW_NAME) / 50 # pixels
    point_list = np.empty((0,2), np.float64)
    x = pxstep
    while x < img.shape[1] // scale:
        y = pxstep
        while y < img.shape[0] // scale:
            # _x = map_x[y,x]            
            # _y = map_y[y,x]
            # point_list = np.c_[point_list, np.array([x,y])]
            point_list = np.vstack([point_list, np.array([[x,y]])])
            y += pxstep
        x += pxstep

    config = get_config()
    new_point_list = rectify.rectify_points(config, point_list, W, H)
    for point in new_point_list:
        cv2.circle(img, (round(point[0]),round(point[1])), 1, (0, 0, 180), 2)

    return img    

    
def save():
    with open(args.config_file, 'w') as f:
        json.dump(get_config(), f)
    print(f"{args.config_file} saved")


while True:

    config = get_config()
    rectify.calc_maps(config, W, H)
    output = rectify.rectify(img)
    
    output = cv2.resize(output, (output.shape[1]//view_scale,output.shape[0]//view_scale))
    output = drawGrid(output, 20)
    output = drawSrcGrid(output, 40)

    cv2.imshow("output",output)
    cv2.waitKey(1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        save()
