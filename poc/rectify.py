import cv2
import numpy as np
import math
import json

map_x,map_y = 0,0

def calc_maps(config, W, H):
    global map_x, map_y

    sensor_h = config['sensor_h']
    sensor_w = config['sensor_w']
    X = config['X']
    Y = config['Y']
    scale = config['scale']
    alpha = config['alpha']
    beta = config['beta']
    gamma = config['gamma']
    focus = config['focus']
    k1, k2, p1, p2 = config['dist']

    Rx = np.array([[1, 0, 0], [0, math.cos(alpha), -math.sin(alpha)], [0, math.sin(alpha), math.cos(alpha)]])
    Ry = np.array([[math.cos(beta), 0, -math.sin(beta)], [0, 1, 0], [math.sin(beta), 0, math.cos(beta)]])
    Rz = np.array([[math.cos(gamma), -math.sin(gamma), 0], [math.sin(gamma), math.cos(gamma), 0], [0, 0, 1]])
    R = np.matmul(Rx, np.matmul(Ry, Rz))
    # T = np.array([[1,0,0,-X],[0,1,0,-Y],[0,0,1,-Z]])
    # RT = np.matmul(R,T)	

    dist = np.array([k1,k2,p1,p2])
    K = np.array([
        [W*focus/sensor_w, 0, W//2],
        [0, H*focus/sensor_h, H//2],
        [0, 0, 1]])
    new_K = np.array([
        [W*focus/sensor_w, 0, scale*W//2 + X],
        [0, H*focus/sensor_h, scale*H//2 + Y],
        [0, 0, 1]])

    map_x, map_y = cv2.initUndistortRectifyMap(K, dist, R, new_K, (round(scale*W),round(scale*H)), 5)

def rectify(img):
    return cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR)

def rectify_points(config, points, W, H):

    sensor_h = config['sensor_h']
    sensor_w = config['sensor_w']
    X = config['X']
    Y = config['Y']
    scale = config['scale']
    alpha = config['alpha']
    beta = config['beta']
    gamma = config['gamma']
    focus = config['focus']
    k1, k2, p1, p2 = config['dist']

    Rx = np.array([[1, 0, 0], [0, math.cos(alpha), -math.sin(alpha)], [0, math.sin(alpha), math.cos(alpha)]])
    Ry = np.array([[math.cos(beta), 0, -math.sin(beta)], [0, 1, 0], [math.sin(beta), 0, math.cos(beta)]])
    Rz = np.array([[math.cos(gamma), -math.sin(gamma), 0], [math.sin(gamma), math.cos(gamma), 0], [0, 0, 1]])
    R = np.matmul(Rx, np.matmul(Ry, Rz))
    # T = np.array([[1,0,0,-X],[0,1,0,-Y],[0,0,1,-Z]])
    # RT = np.matmul(R,T)	

    dist = np.array([k1,k2,p1,p2])
    K = np.array([
        [W*focus/sensor_w, 0, W//2],
        [0, H*focus/sensor_h, H//2],
        [0, 0, 1]])
    new_K = np.array([
        [W*focus/sensor_w, 0, scale*W//2 + X, 0],
        [0, H*focus/sensor_h, scale*H//2 + Y, 0],
        [0, 0, 1, 0]])

    res = cv2.undistortPoints(points, K, dist, R=R, P=new_K)
    return np.reshape(res, (-1,2))    