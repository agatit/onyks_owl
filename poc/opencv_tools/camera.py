import cv2


def frame_capture_gen(film_path):
    vid_obj = cv2.VideoCapture(film_path)

    success = 1
    while success:
        success, image = vid_obj.read()
        if success:
            yield image
