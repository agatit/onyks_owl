import numpy as np
import cv2
import glob
import json
import clipboard
from os.path import join, basename


# Directory for images of chessboards made with custom camera
# camera_cal_in_dir_chessboards = '../../input_images/camera_calibration/H.264/chessboard*.png'

# Directory to which test chessboard images are saved, to prove calibration worked
# camera_cal_out_dir = '../../output_images/H.264/camera_calibration'

# Feature disabled: Filename to save the camera calibration result (mtx, dist)
# calibration_mtx_dist_filename_json = '../../output_images/camera_cal_dist_cache.json'

# Chessboard numbers of internal corners (nx,ny)
# chessboard_size = (9, 6)

# load from config json
def load_camera_mtx_dist_from_json():
    config_json_path = "examples/perspective_transform/config.json"
    config_json = json.load(open(config_json_path, "rb"))
    mtx_lst = config_json["module_perspective_transform"]["params"]["mtx"]
    dist_lst = config_json["module_perspective_transform"]["params"]["dist"]

    mtx = np.array(mtx_lst)
    dist = np.array(dist_lst)

    return mtx, dist


# Assumes config.json location is constant and under examples directory
def get_parameters():
    config_json_path = "../examples/perspective_transform/config.json"
    config_json = json.load(open(config_json_path, "rb"))
    dir_in_chessboards = config_json["module_perspective_transform"]["params"]["camera_cal_in_dir_chessboards"]
    dir_out = config_json["module_perspective_transform"]["params"]["camera_cal_out_dir"]
    chessboard_size = config_json["module_perspective_transform"]["params"]["chessboard_size"]
    return dir_in_chessboards, dir_out, tuple(chessboard_size)


def get_camera_calibration_mtx_dist(camera_cal_in_dir_chessboards, camera_cal_out_dir, chessboard_size):
    '''
    Calibrate camera based on set of chessboard images.
    Undistort one of the images from camera set as a test.
    Save the camera calibration results for later use (mtx,dst)
    '''
    print("Starting calibration process....")

    # Make a list of calibration images
    images = glob.glob(camera_cal_in_dir_chessboards)
    nx, ny = chessboard_size

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((ny * nx, 3), np.float32)
    objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane.

    # Step through the list and search for chessboard corner
    for idx, filename in enumerate(images):
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

        # If found, add object points, image points
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and save images displaying the corners
            cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
            write_name = join(camera_cal_out_dir, "corners_found_" + basename(filename))
            cv2.imwrite(write_name, img)

    img = cv2.imread(images[0])
    img_size = (img.shape[1], img.shape[0])

    # Do camera calibration given object points and image points
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    # Undistort image test and save it
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    write_name1 = join(camera_cal_out_dir, 'Undist_' + basename(images[0]))
    cv2.imwrite(write_name1, dst)

    mtx_list = mtx.tolist()
    dist_list = dist.tolist()
    # saved_obj = {
    #     "mtx": mtx_list,
    #     "dist": dist_list
    # }
    #
    # with open(calibration_mtx_dist_filename_json, 'w', encoding='utf8') as json_file:
    #     json.dump(saved_obj, json_file, indent=3)

    # copied_object = "\"mtx\": " + json.dumps(mtx_list, indent=3) + ",\n" + "\"dist\": " + json.dumps(dist_list,
    #                                                                                                  indent=3)
    copied_object = "\"mtx\": " + str(mtx_list) + ",\n" + "\"dist\": " + str(dist_list)
    print(copied_object)
    clipboard.copy(copied_object)
    print("Mtx and dist saved to clippoard in json format! Copy paste them to config.json.")

    # print("Calibration process complete! [json file saved to: " + calibration_mtx_dist_filename_json + "]")
    print("Undistorted image test: from [" + images[0] + "] to [" + basename(write_name1) + "]")
    print("Here is the undistorted image: [" + write_name1 + "]")


def undistort_test_image(write_name_dir, write_name_img):
    mtx, dist = load_camera_mtx_dist_from_json()
    img = cv2.imread(write_name_dir + '/' + write_name_img)

    # cv2.imshow('image_name', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    dst = cv2.undistort(img, mtx, dist, None, mtx)
    cv2.imwrite(write_name_dir + '/' + 'Undist_' + write_name_img, dst)


if __name__ == '__main__':
    # get_camera_calibration_mtx_dist()
    # undistort_test_image('../../resources', 'train1_Moment.jpg')
    in_dir, out_dir, chessboard = get_parameters()
    get_camera_calibration_mtx_dist(in_dir, out_dir, chessboard)
