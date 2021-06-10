import pickle
import cv2
import numpy as np
from os.path import join, basename
import scipy.spatial.distance
import math

# Program local libraries
# from load_parameters import load_camera_mtx_dist_from_pickle as load_mtx_dist

# Where are the road test images?
railway_test_images_dir = 'input_images/trains'

# Point to a straight road image here
railway_straight_image_filename = 'rect1.jpg'

# Where you want to save warped straight image for check?
railway_straight_warped_image_dir = 'output_images/perpendicular_view_test'

# Where you want to save the transformation matrices (M,Minv)?
M_Minv_output_dir = 'output_images/camera_calibration'

# Notes:
# First there should be a single cargo detection and THEN perspective applied, because the rails are not always straight line

# Sort coordinate points clock-wise, starting from top-left
# Inspired by the following discussion:
# http://stackoverflow.com/questions/1709283/how-can-i-sort-a-coordinate-list-for-a-rectangle-counterclockwise
def order_points(pts):
    # Normalises the input into the [0, 2pi] space, added 0.5*pi to initiate from top left
    # In this space, it will be naturally sorted "counter-clockwise", so we inverse order in the return
    mx = np.sum(pts.T[0] / len(pts))
    my = np.sum(pts.T[1] / len(pts))

    l = []
    for i in range(len(pts)):
        l.append((math.atan2(pts.T[0][i] - mx, pts.T[1][i] - my) + 2 * np.pi + 0.5 * np.pi) % (2 * np.pi))
    sort_idx = np.argsort(l)

    return pts[sort_idx[::-1]]


def get_transform_matrices(pts, img_size):
    # Obtain a consistent order of the points and unpack them individually
    src = order_points(pts)

    # Give user some data to check
    print('Here are the ordered src pts: \n', src)

    # Destination points
    dst = np.float32([[src[3][0], 0],
                      [src[2][0], 0],
                      [src[2][0], img_size[1]],
                      [src[3][0], img_size[1]]])

    # Give user some data to check
    print('Here are the dst pts: \n', dst)

    # Compute the perspective transform matrix and the inverse of it
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    return M, Minv


# def trapezoid_vertices(image, a=(745, 467), b=(745, 203), c=(569, 475), d=(569, 266), bottom_crop_px=0):
#     imshape = image.shape
#
#     trapezoid_h_px = a[1] - b[1]
#
#     # vertices = np.array([[
#     #     (745, 208),
#     #     (745, 470),
#     #     (460, 307),
#     #     (460, 479)]]
#     #     , dtype=np.int32)
#
#     # 4 cargos, no aspect ratio kept
#     vertices = np.array([[
#         (745, 208),
#         (745, 470),
#         (460, 307),
#         (460, 479)]]
#         , dtype=np.int32)
#
#     return vertices

# in current version, this function has the ability to undistort, but doesnt keep aspect ratio
# def get_perspective_and_pickle_M_Minv():
#     # Optimize source points by using straight railway test image
#     # Load image
#     Readname = join(railway_test_images_dir, railway_straight_image_filename)
#     img = cv2.imread(Readname)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#     # Give user some data to check
#     print('Here is the straight image shape: ', img.shape)
#
#     # Load camera coefficients
#     mtx, dist = load_mtx_dist()
#
#     # Undistort and get image size
#     # img = cv2.undistort(img, mtx, dist, None, mtx) # no need if the video is not distorted
#     img_size = (img.shape[1], img.shape[0])
#
#     # trapezoid vertices
#     pts = np.array([[
#         (745, 208),
#         (745, 470),
#         (460, 307),
#         (460, 479)]]
#         , dtype=np.int32)
#
#     # Modify it to expected format
#     pts = pts.reshape(pts.shape[1:])
#     pts = pts.astype(np.float32)
#
#     # Give user some data to check
#     print('Here are the initial src pts: \n', pts)
#
#     # get the transform matrices
#     M, Minv = get_transform_matrices(pts, img_size)
#
#     # transform image and save it
#     warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
#
#     write_name1 = join(railway_straight_warped_image_dir, 'Warped_2' + basename(Readname))
#     cv2.imwrite(write_name1, warped)
#
#     # Save the transformation matrices for later use
#     dist_pickle = {}
#     dist_pickle["M"] = M
#     dist_pickle["Minv"] = Minv
#     write_name2 = join(M_Minv_output_dir, 'perspective_trans_matrices.p')
#     pickle.dump(dist_pickle, open(write_name2, "wb"))
#
#     print('Done!')
#     print("Warped image test: from [" + basename(Readname) + "] to [" + basename(write_name1) + "]")
#     print("Here is the warped image: [" + write_name1 + "]")
#     print("M and Minv saved: [pickled file saved to: " + write_name2 + "]")


def get_perspective_with_aspect_ratio(frame):
    # Readname = join(railway_test_images_dir, railway_straight_image_filename)
    # img = cv2.imread(Readname)
    img = frame
    (rows, cols, _) = img.shape

    # image center
    u0 = (cols) / 2.0
    v0 = (rows) / 2.0

    # detected corners on the original image
    p = []
    # p.append((569, 265))
    # p.append((747, 204))
    # p.append((569, 474))
    # p.append((745, 458))
    p.append((1125, 403))
    p.append((1920, 201))
    p.append((1126, 897))
    p.append((1919, 1055))

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

    dst = cv2.warpPerspective(img, M, (W, H))

    # cv2.imshow('img', img)
    # cv2.imshow('dst', dst)
    # # cv2.imwrite('output_images/perpendicular_view_test/orig1.png', img)
    # cv2.imwrite('output_images/perpendicular_view_test/warp_with_aspect_ratio1.png', dst)
    #
    # cv2.waitKey(0)
    return dst


if __name__ == "__main__":
    Readname = r"C:\Users\Adam P\Documents\GitHub\onyks_owl\input_images\trains\rect1.jpg"
    in_img = cv2.imread(Readname)
    in_transformed = get_perspective_with_aspect_ratio(in_img)
    cv2.imshow('post_transform', in_transformed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()