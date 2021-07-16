import sys
import cv2
import numpy as np
import os

def draw_matches(img1, keypoints1, img2, keypoints2, matches):
        r, c = img1.shape[:2]
        r1, c1 = img2.shape[:2]

        # Create a blank image with the size of the first image + second image
        output_img = np.zeros((max([r, r1]), c+c1, 3), dtype='uint8')
        output_img[:r, :c, :] = np.dstack([img1, img1, img1])
        output_img[:r1, c:c+c1, :] = np.dstack([img2, img2, img2])

        # Go over all of the matching points and extract them
        for match in matches:
            img1_idx = match.queryIdx
            img2_idx = match.trainIdx
            (x1, y1) = keypoints1[img1_idx].pt
            (x2, y2) = keypoints2[img2_idx].pt

            # Draw circles on the keypoints
            cv2.circle(output_img, (int(x1),int(y1)), 4, (0, 255, 255), 1)
            cv2.circle(output_img, (int(x2)+c,int(y2)), 4, (0, 255, 255), 1)

            # Connect the same keypoints
            cv2.line(output_img, (int(x1),int(y1)), (int(x2)+c,int(y2)), (0, 255, 255), 1)
            
        return output_img
def warpImages(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)

    # When we have established a homography we need to warp perspective
    # Change field of view
    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
    
    translation_dist = [-x_min,-y_min]
    
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

    return output_img
def crop(image):

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    # image = cv2.imread('1.jpg')
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (25,25), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Perform morph operations, first open to remove noise, then close to combine
    noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

    # Find enclosing boundingbox and crop ROI
    coords = cv2.findNonZero(np.invert(close))
    x,y,w,h = cv2.boundingRect(coords)
    # cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
    crop = original[y:y+h, x:x+w]

    # cv2.imshow('thresh', thresh)
    # cv2.imshow('close', close)
    # cv2.imshow('image', image)
    # cv2.imshow('crop', crop)
    # cv2.waitKey()
    return crop

cv2.namedWindow("img1_gray", cv2.WINDOW_FREERATIO)
cv2.namedWindow("img2_gray", cv2.WINDOW_FREERATIO)
cv2.namedWindow("keypoints1", cv2.WINDOW_FREERATIO)
cv2.namedWindow("keypoints2", cv2.WINDOW_FREERATIO)
cv2.namedWindow("keypoints3", cv2.WINDOW_FREERATIO)
cv2.namedWindow("keypoints4", cv2.WINDOW_FREERATIO)
cv2.namedWindow("img3", cv2.WINDOW_FREERATIO)
cv2.namedWindow("finale", cv2.WINDOW_FREERATIO)


# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_test_res_len1.avi')
# o_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_V3_test_res_len1_pan.png')
v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39.mp4')
o_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_2_39_pan.png')
# v_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_3_3_V3_test_res_len1.avi')
# o_name = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../samples/youtube/out_3_3_V3_test_res_len1_pan.png')
cap = cv2.VideoCapture(v_name)

# Load our images
# img1 = cv2.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)),"test_full_r.png"))
# img2 = cv2.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)),"test_full_l.png"))

ret, img1 = cap.read()
skipped = 10
for i in range(skipped):
    ret, img2 = cap.read()
while ret:
    # img1_crop = crop(img1)
    # img2_crop = crop(img2)
    # img1_gray = cv2.cvtColor(img1_crop, cv2.COLOR_BGR2GRAY)
    # img2_gray = cv2.cvtColor(img2_crop, cv2.COLOR_BGR2GRAY)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("img1", img1)
    # cv2.imshow("img1_crop", img1_crop)
    # cv2.imshow("img2", img2)
    # cv2.imshow("img2_crop", img2_crop) 
    # cv2.waitKey()
    # cv2.imshow("img1_gray", img1_gray)
    # cv2.imshow("img2_gray", img2_gray)

    # Create our ORB detector and detect keypoints and descriptors
    orb = cv2.ORB_create(nfeatures=2000)

    # Find the key points and descriptors with ORB
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    cv2.imshow("keypoints1", cv2.drawKeypoints(img1, keypoints1, None, (255, 0, 255)))
    cv2.imshow("keypoints2", cv2.drawKeypoints(img2, keypoints2, None, (255, 0, 255)))

    # Create a BFMatcher object.
    # It will find all of the matching keypoints on two images
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

    # Find matching points
    matches = bf.knnMatch(descriptors1, descriptors2,k=2)

    

    all_matches = []
    for m, n in matches:
        all_matches.append(m)

    img3 = draw_matches(img1_gray, keypoints1, img2_gray, keypoints2, all_matches[:30])
    cv2.imshow("img3", img3)

    # Finding the best matches
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)

    cv2.imshow("keypoints3", cv2.drawKeypoints(img1, [keypoints1[m.queryIdx] for m in good], None, (255, 0, 255)))
    cv2.imshow("keypoints4", cv2.drawKeypoints(img2, [keypoints2[m.trainIdx] for m in good], None, (255, 0, 255)))

    # Set minimum match condition
    MIN_MATCH_COUNT = 10
    result = None
    if len(good) > MIN_MATCH_COUNT:
        # Convert keypoints to an argument for findHomography
        src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        # Establish a homography
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        
        result = warpImages(img2, img1, M)
        # result_crop = crop(result)
        cv2.imshow("finale", result)

    k = cv2.waitKey() & 0xFF
    if k == ord('q'):
        break
    # img1 = img2
    if result is not None:
        img1 = np.copy(result)
    # ret, img2 = cap.read()
    for i in range(skipped):
        ret, img2 = cap.read()
cv2.imwrite(o_name, result)
cap.release()