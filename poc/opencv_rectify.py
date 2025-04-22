import json
import multiprocessing
import pickle
from functools import partial
from multiprocessing import Pool
from pathlib import Path

import click
import cv2
import numpy as np
import yaml
from scipy.optimize import minimize

from display.RegionOfInterest import RegionOfInterest
from io_utils.utils import make_clean_dir
from loggers.loggers import init_rich_info_logger
from rectify_optimalization.methods.line_part_selectors.YPoints import YPoints
from rectify_optimalization.objective_functions import rotation_function
from rectify_optimalization.utils import concat_lines
from configs.OpencvRectifyConfig import Cache, OpencvRectifyConfig, load_cv2_bitmask
from opencv_tools.image_generators import ImageGenerator, video_gen, image_dir_gen
from rectify_optimalization.methods.StdMethod import StdMethod
from rectify_optimalization.methods.line_part_selectors.XPoints import XPoints
from rectify_optimalization.methods.line_types.Horizontal import Horizontal
from rectify_optimalization.methods.line_types.Vertical import Vertical

logger = init_rich_info_logger(__name__)


def find_corners(i, image, chessboard_size, output_dir, findChessboardCorners_flags, cornerSubPix_criteria):
    logger.info(f"started processing image: {i}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None, flags=findChessboardCorners_flags)
    # ret, corners = cv2.findChessboardCornersSB(gray, chessboard_size, None, flags=findChessboardCorners_flags)

    if ret is False:
        logger.info(f"not found: {i}")
        return

    logger.info(f"found: {i}")
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), cornerSubPix_criteria)
    # corners.append(corners2)

    original_path = output_dir / f'{i}.jpg'
    cv2.imwrite(original_path, image)

    # Draw and save the corners
    img_chessboard = np.copy(image)
    cv2.drawChessboardCorners(img_chessboard, chessboard_size, corners, ret)
    chessboard_path = output_dir / f'{i}_cb.jpg'
    cv2.imwrite(chessboard_path, img_chessboard)

    return corners


source_types: dict[str, ImageGenerator] = {
    "video": video_gen,
    "image_dir": image_dir_gen,
}


@click.command()
@click.option("-in", "--input", "input_source",
              required=True, type=click.Path(exists=True), help="image or video to rectify")
@click.option("-out", "--output_dir", "output_dir",
              required=True, type=click.Path(), help="rectify config path")
@click.option("-c", '--config', "config_path",
              required=True, type=click.Path(exists=True), default="resources/opencv_rectify.yaml",
              help=f"config file of {OpencvRectifyConfig}")
@click.option("-st", '--source_type', "source_type",
              required=True, type=click.Choice(list(source_types.keys())), help="Input file type flag")
@click.option("-cp", '--cache_path', "cache_paths",
              type=click.Path(exists=True), multiple=True, help="path to cache file, can be multiple")
@click.option("-r", '--rotation_lines_paths', "rotation_lines_paths",
              type=click.Path(exists=True), multiple=True, help="path to json line file, can be multiple")
def main(input_source, output_dir, config_path, source_type, cache_paths, rotation_lines_paths):
    """
    https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
    """
    logger.info(f"started: {__file__}")

    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = OpencvRectifyConfig(**config)

    output_dir = Path(output_dir)
    make_clean_dir(output_dir)

    img_gen = source_types[source_type]

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point in real world space
    img_points = []  # 2d points in image plane.

    # rotations lines
    lines = []

    if len(cache_paths) > 0:
        for catch_path in cache_paths:
            catch_path = Path(catch_path)
            logger.info(f"loading cache: {catch_path}")

            with open(catch_path, "rb") as file:
                cache_dict = pickle.load(file)
                cache = Cache(**cache_dict)

            obj_points += cache.obj_points
            img_points += cache.img_points

    if len(rotation_lines_paths) > 0:
        for path in rotation_lines_paths:
            with open(path, "r") as file:
                lines.append(json.load(file))

        lines = concat_lines(lines)

    if config.gather_points.enable:
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        chessboard_size = config.gather_points.chessboard_size
        objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

        with Pool(processes=config.gather_points.workers) as pool:
            wrapped_task = partial(
                find_corners,
                chessboard_size=chessboard_size,
                output_dir=output_dir,
                findChessboardCorners_flags=load_cv2_bitmask(config.gather_points.findChessboardCorners_flags),
                cornerSubPix_criteria=config.gather_points.cornerSubPix_criteria.to_cv2_criteria_tuple()
            )

            tasks = []
            for i, image in enumerate(img_gen(input_source)):
                if i % config.gather_points.skip_frames != 0:
                    continue

                task = pool.apply_async(wrapped_task, (i, image))
                tasks.append(task)

            for task in tasks:
                result = task.get()

                if result is None:
                    continue

                obj_points.append(objp)
                img_points.append(result)

    if len(img_points) < 1:
        logger.info("found no points to generate rectification")
        return

    if config.gather_points.save_cache:
        try:
            new_cache_path = output_dir / "cache"
            logger.info(f"saving cache: {new_cache_path}")

            cache = Cache(obj_points=obj_points, img_points=img_points)
            with open(new_cache_path, "wb") as file:
                pickle.dump(cache.model_dump(), file)

        except Exception:
            logger.error("unable to save cache")

    logger.info(f"calibrating focal and optical center")

    camera = config.camera
    h, w = camera.height, camera.width
    fx, fy = camera.fx, camera.fy
    cx, cy = camera.cx, camera.cy
    init_camera_matrix = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, (w, h), init_camera_matrix,
        distCoeffs=np.array(config.calibrateCamera.distCoeffs),
        flags=load_cv2_bitmask(config.calibrateCamera.flags),
        criteria=config.calibrateCamera.criteria.to_cv2_criteria_tuple()
    )

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (w, h),
        newImgSize=(w, h),
        **config.getOptimalNewCameraMatrix
    )

    # rotation
    alpha, beta, gamma = (0.0, 0.0, 0.0)

    if config.rectify.enable and len(lines) > 0:
        logger.info(f"calibrating rotation")

        roi = RegionOfInterest(
            source_region_size=(config.camera.width, config.camera.height),
            x1=0,
            y1=0,
            x2=config.camera.width,
            y2=config.camera.height,
        )

        horizontal_method = StdMethod(lines, 1, Horizontal(), YPoints(), roi)
        vertical_method = StdMethod(lines, 1, Vertical(), XPoints(), roi)
        methods = [horizontal_method, vertical_method]

        objective_function = partial(
            rotation_function,
            methods=methods,
            camera_matrix=mtx,
            dist=dist,
            new_camera_matrix=newcameramtx
        )

        x0 = list(config.rotate.init.values())
        bound = list(config.rotate.bounds.values())
        res = minimize(objective_function, x0, bounds=bound, **config.rotate.minimize_kwargs)

        # res = minimize(objective_function, x0, **config.rotate.minimize_kwargs)

        logger.info(f"init guess fun value: {objective_function(x0)}" )
        logger.info(f"Found fun value: {res.fun}" )
        alpha, beta, gamma = res.x

    R, jac = cv2.Rodrigues(np.array([alpha, beta, gamma]))
    mapx, mapy = cv2.initUndistortRectifyMap(
        mtx, dist, R, newcameramtx, (w, h), 5
    )

    # results.json
    result_path = output_dir / "results.json"
    logger.info(f"generating result file: {result_path}")

    R_ = cv2.Rodrigues(R)[0].tolist()
    result: dict[str, any] = {
        "input_config": config.model_dump(),
        "ret": ret,
        "mtx": mtx.tolist(),
        "dist": dist.tolist(),
        "newcameramtx": newcameramtx.tolist(),
        "R": R_,
    }

    with open(result_path, "w") as file:
        json.dump(result, file)

    # # rectify.json
    # result_path = output_dir / "rectify.json"
    # logger.info(f"generating rectify file: {result_path}")
    #
    # focal_mm = config.camera.focal_mm
    # result: dict[str, any] = {
    #     'sensor_w': focal_mm * w / mtx[0][0],
    #     'sensor_h': focal_mm * h / mtx[1][1],
    #     # 'sensor_w':
    # }
    #
    # focus_w = mtx[0][0]
    # with open(result_path, "w") as file:
    #     json.dump(result, file)

    if config.generate_mapx_mapy:
        result_path = output_dir / "mapx_mapy.pkl"
        logger.info(f"generating mapx mapy result file: {result_path}")

        mapx_mapy = {
            "mapx": mapx,
            "mapy": mapy,
        }

        with open(result_path, "wb") as file:
            pickle.dump(mapx_mapy, file)

    if config.rectify.enable:
        logger.info("rectifying images")

        # x, y, w, h = roi
        for i, image in enumerate(img_gen(input_source)):
            if i % config.rectify.skip_frames != 0:
                continue

            dst = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
            # dst = cv2.remap(dst, mapx, mapy, cv2.INTER_LINEAR)
            # dst = dst[y:y + h, x:x + w]

            rectified_path = output_dir / f'{i}_r.jpg'
            # logger.info(f"saving: {rectified_path}")
            cv2.imwrite(rectified_path, dst)


if __name__ == '__main__':
    # PyInstaller - https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html#multi-processing
    multiprocessing.freeze_support()
    main()
