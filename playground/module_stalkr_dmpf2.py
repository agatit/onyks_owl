# Source - https://docs.opencv.org/4.5.2/d3/d14/tutorial_ximgproc_disparity_filtering.html

import cv2
import os

########    INPUT DATA    ########
left_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/ambush_5_left.jpg')
right_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/ambush_5_right.jpg')
 
# left_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/tsukuba_l.png')
# right_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/tsukuba_r.png')

# left_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para2_01.jpg')
# right_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para2_02.jpg')

# left_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para_01.jpg')
# right_im = os.path.join(os.path.abspath(os.path.dirname(__file__)),'./photo/para_02.jpg')

######## ENDOF INPUT DATA ########

"""   Zmienne/parametry   """
max_disp = 16           # wartość maksymalna różnicy
wsize = 15              # rozmiar bloku porównującego
# lambada = 8000.0        # default - 8000
# sigma = 1.5             # default - <0.8;2.0>
# sigma = 15              # default - <0.8;2.0>
vis_mult = 1.0          # mnożnik skali wizualizacji
window_title = 'Title'  # nazwa okna
# trackbar_name = 'track' # nazwa paska

trackbar_sigma_max = 20
trackbar_sigma = 'Sigma / %d' % 10
trackbar_lambada_max = 200
trackbar_lambada = 'Lambda x %d' % 100

# trackbar_sigma / 10 = sigma
# trackbar_lambada * 100 = lambada


def load_images():
    left = cv2.imread(left_im, cv2.IMREAD_COLOR)
    if left is None:
        print("Cannot read image file: ", left_im)
        exit(0)

    right = cv2.imread(right_im, cv2.IMREAD_COLOR)
    if right is None:
        print("Cannot read image file: ", right_im)
        exit(0)
    
    return left, right

def resize_image(image):
    image_resized  = cv2.resize(src = image,
                                dsize = (0,0),
                                fx = 0.5,
                                fy = 0.5,
                                interpolation = cv2.INTER_LINEAR_EXACT)
    return image_resized

def do_dis_shit(left, right, sigma, lambada): # TODO zmienić nazwę
    left_matcher = cv2.StereoBM_create(                           
                                        numDisparities = max_disp,
                                        blockSize = wsize         
                                      )
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher) 

    left_for_matcher = cv2.cvtColor(src = left,   code = cv2.COLOR_BGR2GRAY)   
    right_for_matcher = cv2.cvtColor(src = right, code = cv2.COLOR_BGR2GRAY)


    left_disp = left_matcher.compute(left_for_matcher, right_for_matcher) # Obliczanie "mapy rozbieżności"
    right_disp = right_matcher.compute(right_for_matcher,left_for_matcher)

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher) # Stworzenie obiektu filtra WLS
    wls_filter.setLambda(lambada) # przyległość do krawędzi ?
    wls_filter.setSigmaColor(sigma) # czułość na krawędziach ?
    filtered_disp = wls_filter.filter(  disparity_map_left = left_disp,
                                        left_view = left,
                                        disparity_map_right = right_disp)


    filtered_disp_vis = cv2.ximgproc.getDisparityVis(src = filtered_disp, scale = vis_mult)

    return filtered_disp_vis

def sliders_track(val):
    sigma = cv2.getTrackbarPos(trackbar_sigma, window_title) / 10.0
    lambada = cv2.getTrackbarPos(trackbar_lambada, window_title) * 100
    image = do_dis_shit(resize_image(left), resize_image(right), sigma, lambada)
    # image = do_dis_shit(left, right, sigma, lambada)
    cv2.imshow(window_title, image)

def trackbar_init():

    cv2.namedWindow(window_title)

    cv2.createTrackbar(trackbar_sigma, window_title , 15, trackbar_sigma_max, sliders_track)
    cv2.createTrackbar(trackbar_lambada, window_title , 80, trackbar_lambada_max, sliders_track)

if __name__ == "__main__":
    left, right = load_images()
    trackbar_init()
    # TODO max_disp & wsize - suwaki
    # TODO wielkości zdjęć
        # zmniejszać je do X (np. HD)
        # dać możliwość żeby ogarniać zmiejszone albo nie

    # left_resized = resize_image(left)
    # right_resized = resize_image(right)
    # result = do_dis_shit(left_resized, right_resized)
    cv2.waitKey()

