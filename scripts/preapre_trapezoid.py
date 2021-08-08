import sys
from pathlib import Path

if __name__ == '__main__' and __package__ is None:
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[1]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # Already removed
        pass
    __package__ = 'onyks_owl'

import json
import logging
import cv2
import numpy as np
import argparse
import clipboard

from owl.perspective.perspective_transform import order_points, order_points_clockwise
from scripts.camera_calibration import load_camera_mtx_dist_from_json as load_mtx_dist

# GLOBALS
# global list that stores [x, y] points that were left-clicked
left_clicks = list()
scaled_clicks = list()
global global_frame


# https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# video_percentage -- which frame of the video do you want to read,
# eg. 50 means 50% of the video, so in the middle
def get_frame_from_video(filename, video_percentage):
    logging.info(f"filename {filename}")

    # Open the video file
    cap = cv2.VideoCapture(filename)

    # Get fps, frame count of the opened video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # frame_seq = int((frame_count - 1)
    frame_no = int((frame_count - 1) * float(video_percentage / 100))
    time_length = frame_count / fps
    print(f"fps: {fps}, frame_count: {frame_count}, time_length: {time_length}")

    # number of the video frame that you want to edit
    cap.set(1, frame_no)

    # Read the next frame from the video
    ret, frame = cap.read()

    # Cut the video extension to have the name of the video
    video_name = filename.split(".")[0]

    # # Display the resulting frame
    frame_name = video_name + ' frame ' + str(frame_no)
    # cv2.imshow(frame_name, frame)
    #
    # # Set waitKey
    # cv2.waitKey()
    #
    # # Store this frame to an image
    # cv2.imwrite(video_name + '_frame_' + str(frame_seq) + '.jpg', frame)

    # When everything done, release the capture
    cap.release()
    # cv2.destroyAllWindows()
    return frame, frame_name


def on_mouse_event(event, x, y, flags, param):
    global global_frame
    frame = param[0]
    frame_name = param[1]
    scale = param[2]

    if event == cv2.EVENT_LBUTTONUP:
        if len(left_clicks) < 4:
            left_clicks.append([x, y])
            scaled_x = int(x / float(scale))
            scaled_y = int(y / float(scale))
            scaled_clicks.append([scaled_x, scaled_y])
            frame_canvas = frame.copy()
            for point, scaled_points in zip(left_clicks, scaled_clicks):
                x = point[0]
                y = point[1]
                scaled_x = scaled_points[0]
                scaled_y = scaled_points[1]
                xy = "%d,%d" % (scaled_x, scaled_y)
                cv2.circle(frame_canvas, (x, y), 2, (255, 0, 0), thickness=-1)
                cv2.putText(frame_canvas, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0, 0, 0), thickness=1)
            if len(left_clicks) == 4:
                pts = np.array(left_clicks)
                scaled_pts = np.array(scaled_clicks)

                ordered_scaled_pts = order_points(scaled_pts)
                copied_object = json.dumps(ordered_scaled_pts.tolist())
                print(copied_object)
                clipboard.copy(copied_object)
                print("Trapezoid coords have been copied to clipboard!")

                ordered_pts = order_points_clockwise(pts)
                ordered_pts = ordered_pts.reshape((-1, 1, 2))
                cv2.polylines(frame_canvas, [ordered_pts], True, (0, 255, 255))

            # update global frame which is passed to main to be displayed
            global_frame = frame_canvas.copy()
            #print(left_clicks)
            if len(left_clicks) > 4:
                print("Alert! You don't need more than 4 coords! Delete some.")
    if event == cv2.EVENT_RBUTTONUP:
        if len(left_clicks) > 0:
            left_clicks.pop()
        else:
            print("Alert! Can't delete coords if there are none!")

        frame_canvas = frame.copy()
        for point in left_clicks:
            x = point[0]
            y = point[1]
            scaled_x = int(x / float(scale))
            scaled_y = int(y / float(scale))
            xy = "%d,%d" % (scaled_x, scaled_y)
            cv2.circle(frame_canvas, (x, y), 2, (255, 0, 0), thickness=-1)
            cv2.putText(frame_canvas, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
        # update global frame
        global_frame = frame_canvas.copy()
        #print(left_clicks)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Visual trapezoid editor')
    parser.add_argument('filename', type=str, help='video file')
    parser.add_argument('-u', '--undisort', dest="undisort", action='store_true', help='undisort video')
    parser.add_argument('-s', '--scale', dest="scale", type=int, default=50, help='scale factor for display')
    args = parser.parse_args()
    print(args)   

    pause = False
    first = True
    cap = cv2.VideoCapture(args.filename) 
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.namedWindow(args.filename)

    grabbed, frame = cap.read()

    while grabbed:
        if args.scale < 100:
            #TODO: calculate scale
            h, w = frame.shape[:2]
            scale_width = 1200 / float(w)
            scale_height = 675 / float(h)
            scale = min(scale_width, scale_height)
            window_width = int(frame.shape[1] * scale)
            window_height = int(frame.shape[0] * scale)

            frame = cv2.resize(frame, (window_width, window_height), interpolation=cv2.INTER_AREA)

        if args.undisort:
            mtx, dist = load_mtx_dist()
            frame = cv2.undistort(frame, mtx, dist, None, mtx)

        
        if not pause:
            global_frame = frame
            params = [frame, args.filename, scale]
        
        cv2.imshow(args.filename, global_frame)

        key = cv2.waitKey(int(1000/fps))
        if key == ord(" "):
            pause = not pause
            if pause:
                cv2.setMouseCallback(args.filename, on_mouse_event, param=params)
            else:
                cv2.setMouseCallback(args.filename, lambda *args : None) 
                left_clicks = list()
                scaled_clicks = list()

        if  key == ord('q'):
            break
        
        if not pause:
            grabbed, frame = cap.read()

    cv2.destroyAllWindows()
