import numpy as np
from PIL import Image
import time
import matplotlib.pyplot as plt
import os

from process import Process


image_path_left = os.path.join(os.path.abspath(os.path.dirname(__file__)),'photo/ambush_5_left.jpg')
image_path_right = os.path.join(os.path.abspath(os.path.dirname(__file__)),'photo/ambush_5_right.jpg')

imL = Process(image_path_left)
imL.resize_image(357, 250)
arrL = imL.get_array()
imL.get_info()

imR = Process(image_path_right)
imR.resize_image(357, 250)
arrR = imR.get_array()
imR.get_info()

from scipy import ndimage

# activate for laplacian filter
arrL_filtered = ndimage.laplace(arrL)
arrR_filtered = ndimage.laplace(arrR)

array_left = arrL
array_right = arrR

"""
Calculate Disparity using Sum of Absolute Differences Method (SAD)
__________________________________________________________________

Region matching between windows in the left and right images using the SAD method. 
Modify 'size' and 'search_range' to alter results.
"""

size = 11

search_range = 44

start_time = time.time()

disp_matrix = []

for row in range(len(arrL_filtered) - size):

    if row % 10 == 0:
        print(f"{row} rows completed.")

    disps = []

    for col1 in range(len(arrL_filtered[row]) - size):
        win1 = arrL_filtered[row:row + size, col1:col1 + size].flatten()

        if col1 < search_range:
            init = 0
        else:
            init = col1 - search_range

        sads = []

        for col2 in range(col1, init - 1, -1):
            win2 = arrR_filtered[row:row + size, col2:col2 + size].flatten()

            sad = np.sum(np.abs(np.subtract(win1, win2)))
            sads.append(sad)

        disparity = np.argmin(sads)
        disps.append(disparity)

    disp_matrix.append(disps)
            
        
disp_matrix = np.array(disp_matrix)

end_time = time.time()

print(f"Total runtime: {end_time - start_time}")
print(disp_matrix.shape)

"""
Recycle Bin Image Calibration
_____________________________

Calculate the z-coordinate for each pixel using constants in 'calib.txt'
"""

z_matrix = np.copy(disp_matrix)

for i in np.nditer(z_matrix):
    i = 178.232 * 2945.377 / (i + 170.681)


"""
Optional: Save matrix in a .pkl file for future usage.
"""

import pickle

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'./data/output/z.pkl', 'wb')) as f:
    pickle.dump(z_matrix, f)

"""
Post-processing
_______________

Take the output matrix from disparity calculations and handle noise and discontinuities.

Noise:

    - Mode Method: Calculate the mode value in a large window around each pixel; assign to value if exceeds threshold.

    - Threshold Cutoff Method: Flatten any extraneous pixels above a threshold to a preset value.

Discontinuity:

    - Average Method: Calculate the average in small window around each pixel; assign value if difference between disparity
                      and value exceed a threshold.

"""

from process import Process

import pandas as pd
from scipy import stats

raw_img = os.path.join(os.path.abspath(os.path.dirname(__file__)),'photo/ambush_5_left.jpg')

img = Image.open(raw_img)
img = img.resize((disp_matrix.shape[1], disp_matrix.shape[0]))
arr = np.array(img)

xyzrgb = []

avg_disp = np.copy(disp_matrix)

for x in range(disp_matrix.shape[1]):
    for y in range(disp_matrix.shape[0]):

        # MEAN
        avg = np.mean(avg_disp[y-7:y+8, x-7:x+8])
        if avg_disp[y, x] - avg > 5:
            avg_disp[y, x] = avg

        # MODE
        if x > 12 and x < 227:
            if avg_disp[y, x] > 25:
                mode = stats.mode(avg_disp[y-12:y+13, x-12:x+13].flatten())
                avg_disp[y, x] = mode[0][0]

        # THRESHOLD
        if avg_disp[y, x] > 30:
            avg_disp[y, x] = 25

        z = np.multiply(avg_disp[y, x], 6)
        rgb = arr[y, x].astype(np.float) / 255.0
        xyzrgb.append([x, y, z])

df = pd.DataFrame(xyzrgb)
df.columns = ['x', 'y', 'z']
df.to_csv('./data/output/point_cloud.txt', index=False)
plt.imshow(avg_disp)
plt.savefig('./data/output/disp_MPL.png')



import open3d as o3d


# filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),'z.pkl')
# filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),'point_cloud.txt')
print("Load a ply point cloud, print it, and render it")
# pcd = o3d.io.read_point_cloud("../../TestData/fragment.ply")
# pcd = o3d.io.read_point_cloud(filename, format = 'xyz', remove_nan_points=False, remove_infinite_points=False, print_progress= True)
# pcd = o3d.io.read_point_cloud("./point_cloud.txt", format = 'xyzrgb')

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyzrgb)

print(pcd)
print(np.asarray(pcd.points))
o3d.visualization.draw_geometries([pcd])

print("Downsample the point cloud with a voxel of 0.05")
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
o3d.visualization.draw_geometries([downpcd])

print("Recompute the normal of the downsampled point cloud")
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    radius=0.1, max_nn=30))
o3d.visualization.draw_geometries([downpcd])

print("Print a normal vector of the 0th point")
print(downpcd.normals[0])
print("Print the normal vectors of the first 10 points")
print(np.asarray(downpcd.normals)[:10, :])
print("")

print("Load a polygon volume and use it to crop the original point cloud")
vol = o3d.visualization.read_selection_polygon_volume(
    "../../TestData/Crop/cropped.json")
chair = vol.crop_point_cloud(pcd)
o3d.visualization.draw_geometries([chair])
print("")

print("Paint chair")
chair.paint_uniform_color([1, 0.706, 0])
o3d.visualization.draw_geometries([chair])
print("")