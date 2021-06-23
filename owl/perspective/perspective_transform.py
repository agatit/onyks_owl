import pickle
import cv2
import numpy as np
from os.path import join, basename
import scipy.spatial.distance
import math


def get_perspective_Mtx_with_aspect_ratio(frame, points):
    img = frame
    (rows, cols, _) = img.shape

    # image center
    u0 = (cols) / 2.0
    v0 = (rows) / 2.0

    # detected corners on the original image
    # TO DO -- load points from config.json
    #       -- get points based on the angle and distance of the camera
    # p = []
    # p.append((1125, 403))
    # p.append((1920, 201))
    # p.append((1126, 897))
    # p.append((1919, 1055))
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

    # calculate the focal distance
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

    f = math.sqrt(np.abs((1.0 / (n23 * n33)) * ((n21 * n31 - (n21 * n33 + n23 * n31) * u0 + n23 * n33 * u0 * u0) + (
                n22 * n32 - (n22 * n33 + n23 * n32) * v0 + n23 * n33 * v0 * v0))))

    A = np.array([[f, 0, u0], [0, f, v0], [0, 0, 1]]).astype('float32')

    At = np.transpose(A)
    Ati = np.linalg.inv(At)
    Ai = np.linalg.inv(A)

    # calculate the real aspect ratio
    ar_real = math.sqrt(np.dot(np.dot(np.dot(n2, Ati), Ai), n2) / np.dot(np.dot(np.dot(n3, Ati), Ai), n3))

    if ar_real < ar_vis:
        W = int(w)
        H = int(W / ar_real)
    else:
        H = int(h)
        W = int(ar_real * H)

    pts1 = np.array(p).astype('float32')
    pts2 = np.float32([[0, 0], [W, 0], [0, H], [W, H]])

    # project the image with the new w/h
    M = cv2.getPerspectiveTransform(pts1, pts2)

    # dst = cv2.warpPerspective(img, M, (W, H))

    # cv2.imshow('img', img)
    # cv2.imshow('dst', dst)
    # # cv2.imwrite('output_images/perpendicular_view_test/orig1.png', img)
    # cv2.imwrite('output_images/perpendicular_view_test/warp_with_aspect_ratio1.png', dst)
    #
    # cv2.waitKey(0)
    # return dst
    return M, W, H


if __name__ == "__main__":
    Readname = r"C:\Users\Adam P\Documents\GitHub\onyks_owl\input_images\trains\rect1.jpg"
    in_img = cv2.imread(Readname)
    #in_transformed = get_perspective_with_aspect_ratio(in_img)
    M, W, H = in_transformed = get_perspective_with_aspect_ratio(in_img)
    in_transformed = cv2.warpPerspective(in_img, M, (W, H))
    cv2.imshow('post_transform', in_transformed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()