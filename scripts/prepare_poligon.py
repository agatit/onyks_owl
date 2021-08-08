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
global_frame = []


def on_mouse_event(event, x, y, flags, param):
    global global_frame
    global left_clicks
    global scaled_clicks
    frame = param[0]
    frame_name = param[1]
    scale = param[2]

    if event == cv2.EVENT_LBUTTONUP:
        left_clicks.append([x, y])
        scaled_x = int(x / float(scale))
        scaled_y = int(y / float(scale))
        scaled_clicks.append([scaled_x, scaled_y])

    if event == cv2.EVENT_RBUTTONUP:
        
        scaled_pts = np.array(scaled_clicks)

        copied_object = json.dumps(scaled_pts.tolist())
        print(copied_object)
        clipboard.copy(copied_object)
        print("Trapezoid coords have been copied to clipboard!")
        left_clicks = []
        scaled_clicks = []


    if event in [cv2.EVENT_RBUTTONUP, cv2.EVENT_LBUTTONUP]:
        pts = np.array(left_clicks)

        frame_canvas = frame.copy()
        cv2.polylines(frame_canvas, [pts], True, (0, 255, 255))
        
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
