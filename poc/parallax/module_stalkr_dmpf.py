# dmpf - Disparity map post-filtering 
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
max_disp = 16       # wartość maksymalna różnicy
wsize = 15          # rozmiar bloku porównującego
lambada = 20000.0    # default - 8000
sigma = 1.5         # default - <0.8;2.0>
vis_mult = 1.0      # mnożnik skali wizualizacji


"""   Wczytanie zdjęć   """
left = cv2.imread(left_im, cv2.IMREAD_COLOR)
if left is None:
    print("Cannot read image file: ", left_im)
    exit(0)

right = cv2.imread(right_im, cv2.IMREAD_COLOR)
if right is None:
    print("Cannot read image file: ", right_im)
    exit(0)

"""   Ustawienie 'maksymalnej wartości różnicy'   """
max_disp/=2
if max_disp%16!=0:
    max_disp += 16-(max_disp%16)
max_disp = int(max_disp)



"""   Zmniejszenie rozmiarów zdjęć   """
left_for_matcher  = cv2.resize( src = left,
                                dsize = (0,0),
                                fx = 0.5,
                                fy = 0.5,
                                interpolation = cv2.INTER_LINEAR_EXACT)
right_for_matcher = cv2.resize( src = right,
                                dsize = (0,0),
                                fx = 0.5,
                                fy = 0.5,
                                interpolation = cv2.INTER_LINEAR_EXACT)
# cv2.imshow("left_for_matcher", left_for_matcher)
# cv2.imshow("right_for_matcher", right_for_matcher)
# cv2.waitKey()

"""   Przetwarzanie zdjęć   """
left_matcher = cv2.StereoBM_create(                             # Stworzenie obiektu StereoBM
                                    numDisparities = max_disp,  # Maksymalna wartość różnicy
                                    blockSize = wsize           # Rozmiar bloku porównującego
                                  )
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher) # Stworzenie obiektu StereoMatcher

left_for_matcher = cv2.cvtColor(src = left_for_matcher,   code = cv2.COLOR_BGR2GRAY)    # zmiana kolorystyki zdjęcia na czarno-białą
                                                                                        # potem na podstawie tych zdjęć będą tworzone "mapy rozbieżności" 
right_for_matcher = cv2.cvtColor(src = right_for_matcher, code = cv2.COLOR_BGR2GRAY)

# cv2.imshow("left_for_matcher", left_for_matcher)
# cv2.imshow("right_for_matcher", right_for_matcher)
# cv2.waitKey()

left_disp = left_matcher.compute(left_for_matcher, right_for_matcher) # Obliczanie "mapy rozbieżności"
right_disp = right_matcher.compute(right_for_matcher,left_for_matcher)

raw_disp_vis = cv2.ximgproc.getDisparityVis(src = left_disp, scale = vis_mult)  # wizualizacja mapy rozbieżności
                                                                                # wzięcie efektu filtracji i przeskalowanie go w górę z powrotem ?
# norm_imagel = cv2.normalize(left_disp, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
# norm_imager = cv2.normalize(right_disp, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
# cv2.imshow("norm_imagel", norm_imagel)
# cv2.imshow("norm_imager", norm_imager)
# cv2.waitKey()

"""   Filtr 'Weighted Least Squares'   """
wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher) # Stworzenie obiektu filtra WLS
wls_filter.setLambda(lambada) # przyległość do krawędzi ?
wls_filter.setSigmaColor(sigma) # czułość na krawędziach ?
filtered_disp = wls_filter.filter(  disparity_map_left = left_disp,     # mapa rozbieżności lewego widoku
                                    left_view = left,                   # lewy widok
                                    disparity_map_right = right_disp)   # mapa rozbieżności prawego widoku, opcjonalna


filtered_disp_vis = cv2.ximgproc.getDisparityVis(src = filtered_disp, scale = vis_mult) # wizualizacja mapy rozbieżności
                                                                                        # wzięcie efektu filtracji i przeskalowanie go w górę z powrotem ?


"""   Wyświetlanie   """
cv2.namedWindow("raw disparity", cv2.WINDOW_AUTOSIZE)
cv2.imshow("raw disparity", raw_disp_vis)


cv2.imshow("filtered disparity", filtered_disp_vis)
cv2.waitKey(0)

# while 1:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# TODO spróbować StereoSGBM zamiast StereoBM


"""   Suwak   """
# def on_trackbar(value):
#     alpha = val / alpha_slider_max
#     beta = ( 1.0 - alpha )
#     dst = cv2.addWeighted(src1, alpha, src2, beta, 0.0)
#     cv2.imshow(title_window, dst)

# cv2.namedWindow("filtered disparity", cv2.WINDOW_AUTOSIZE)

# alpha_slider_max = 100
# trackbar_name = 'Alpha x %d' % alpha_slider_max

# cv2.createTrackbar(trackbar_name, "filtered disparity" , 0, alpha_slider_max, on_trackbar)
