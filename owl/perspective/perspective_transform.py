import cv2
import numpy as np
import scipy.spatial.distance
import math


# modified answer https://stackoverflow.com/a/38402378 https://creativecommons.org/licenses/by-sa/4.0/
# calculations based on paper:
# https://www.microsoft.com/en-us/research/uploads/prod/2016/11/Digital-Signal-Processing.pdf
def get_perspective(frame, points):
    (rows, cols, _) = frame.shape

    # image center
    u0 = cols / 2.0
    v0 = rows / 2.0

    # PerspectiveTransform() requires points to be passed in a specific order
    points = order_points(points)

    # append corners of the trapezoid [projected image]
    p = []
    for point in points:
        p.append(point)

    # widths and heights of the projected image
    w1 = scipy.spatial.distance.euclidean(p[0], p[1])
    w2 = scipy.spatial.distance.euclidean(p[2], p[3])

    h1 = scipy.spatial.distance.euclidean(p[0], p[2])
    h2 = scipy.spatial.distance.euclidean(p[1], p[3])

    w = max(w1, w2)
    h = max(h1, h2)

    # visible aspect ratio
    ar_vis = float(w) / float(h)

    # make numpy arrays and append 1 for linear algebra
    m1 = np.array((p[0][0], p[0][1], 1)).astype('float32')
    m2 = np.array((p[1][0], p[1][1], 1)).astype('float32')
    m3 = np.array((p[2][0], p[2][1], 1)).astype('float32')
    m4 = np.array((p[3][0], p[3][1], 1)).astype('float32')

    # calculate the focal length f
    k2 = np.dot(np.cross(m1, m4), m3) / np.dot(np.cross(m2, m4), m3)
    k3 = np.dot(np.cross(m1, m4), m2) / np.dot(np.cross(m3, m4), m2)

    n2 = k2 * m2 - m1
    n3 = k3 * m3 - m1

    n21 = n2[0]
    n22 = n2[1]
    n23 = n2[2]

    n31 = n3[0]
    n32 = n3[1]
    n33 = n3[2]

    # calculate the real aspect ratio
    if k2 == 1 and k3 == 1:
        ar_real = math.sqrt((n21 ** 2 + n22 ** 2) / (n31 ** 2 + n32 ** 2))
    else:
        f = math.sqrt(np.abs((1.0 / (n23 * n33)) * ((n21 * n31 - (n21 * n33 + n23 * n31) * u0 + n23 * n33 * u0 * u0) + (
                n22 * n32 - (n22 * n33 + n23 * n32) * v0 + n23 * n33 * v0 * v0))))

        A = np.array([[f, 0, u0], [0, f, v0], [0, 0, 1]]).astype('float32')

        At = np.transpose(A)
        Ati = np.linalg.inv(At)
        Ai = np.linalg.inv(A)

        ar_real = math.sqrt(np.dot(np.dot(np.dot(n2, Ati), Ai), n2) / np.dot(np.dot(np.dot(n3, Ati), Ai), n3))

    # scale w/h of the trapezoid into new W/H of the real image
    # here: scaling down [the shorter rectangle's edge is shortened, the longer edge is scaled to the shorter]
    # won't work when h/ar_real<1 or w*ar_real<1 [so for a very short length in pixels]
    if ar_real > ar_vis:
        H = int(h / ar_real)
        W = int(h)
    else:
        W = int(w * ar_real)
        H = int(w)

    pts1 = np.array(p).astype('float32')
    pts2 = np.float32([[0, 0], [W, 0], [0, H], [W, H]])

    # project the image with the new w/h
    M = cv2.getPerspectiveTransform(pts1, pts2)

    return M, W, H


# Sort coordinates clock-wise, starting from top-left, then revert the order of last two
# PerspectiveTransform() requires first two points being clock-wise (starting top-left) and
# ...last two points being counter-clock-wise (starting left-bottom)
# http://stackoverflow.com/questions/1709283/how-can-i-sort-a-coordinate-list-for-a-rectangle-counterclockwise
def order_points(pts):
    pts = pts.astype(np.float32)
    # Normalises the input into the [0, 2pi] space, added 0.5*pi to initiate from top left
    # In this space, it will be naturally sorted "counter-clockwise", so we inverse order in the return
    mx = np.sum(pts.T[0] / len(pts))
    my = np.sum(pts.T[1] / len(pts))

    l = []
    for i in range(len(pts)):
        l.append((math.atan2(pts.T[0][i] - mx, pts.T[1][i] - my) + 2 * np.pi + 0.5 * np.pi) % (2 * np.pi))
    sort_idx = np.argsort(l)

    # assumes there will always be 4 trapezoid vertices
    sort_idx = sort_idx[::-1]
    sort_idx_1 = sort_idx[0:2:1]
    sort_idx_2 = sort_idx[4:1:-1]

    sort_idx = np.concatenate((sort_idx_1, sort_idx_2))
    return pts[sort_idx].astype(np.int32)


def order_points_clockwise(pts):
    pts = pts.astype(np.float32)
    # Normalises the input into the [0, 2pi] space, added 0.5*pi to initiate from top left
    # In this space, it will be naturally sorted "counter-clockwise", so we inverse order in the return
    mx = np.sum(pts.T[0] / len(pts))
    my = np.sum(pts.T[1] / len(pts))

    l = []
    for i in range(len(pts)):
        l.append((math.atan2(pts.T[0][i] - mx, pts.T[1][i] - my) + 2 * np.pi + 0.5 * np.pi) % (2 * np.pi))
    sort_idx = np.argsort(l)

    return pts[sort_idx[::-1]].astype(np.int32)
