import numpy as np


class CarStitcherRoi:
    def __init__(self, roi_size=(0, 0, 0, 0)):

        self.x = 0  # pozycja ostatniej pełnej ramki względem canvy
        self.y = 0

        self.roi = roi_size

        self.canva = None
        self.alpha = None

    def next(self, frame, velocity):
        velocity_x, velocity_y = velocity
        h_f, w_f, _ = frame.shape

        if self.canva is None or velocity == (0, 0):
            "przypisanie pierwszej klatki do canvy"
            self.canva = frame
            self.alpha = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint16)
            return frame

        roi = frame[self.roi[1]:h_f - self.roi[3], self.roi[0]:w_f - self.roi[2]]
        h_r, w_r, _ = roi.shape  # shape of roi

        self.x -= velocity_x
        self.y -= velocity_y
        x_r = int(self.x) + self.roi[0]
        y_r = int(self.y) + self.roi[1]
        x_f = int(self.x)
        y_f = int(self.y)

        # rozszerzanie canvy i alphy do odpowiedniego polozenia zdjecia
        w_c, h_c, _ = self.canva.shape
        if x_f + w_f > h_c:
            "Przesuniecie canvy w lewo - uzupełninie z prawej"
            self.canva = np.hstack((self.canva, np.zeros((w_c, x_f + w_f - h_c, 3), np.uint8)))
            self.alpha = np.hstack((self.alpha, np.zeros((w_c, x_f + w_f - h_c, 1), np.uint16)))

        w_c, h_c, _ = self.canva.shape
        if x_f < 0:
            "Przesuniecie canvy w prawo - uzupełnienie z lewej, korekta ofsetu"
            self.canva = np.hstack((np.zeros((w_c, -x_f, 3), np.uint8), self.canva))
            self.alpha = np.hstack((np.zeros((w_c, -x_f, 1), np.uint16), self.alpha))
            self.x -= x_f  # ~0
            x_r = self.roi[0]
            x_f = 0

        # uzupełnianie pionu
        w_c, h_c, _ = self.canva.shape
        if y_f + h_f > w_c:
            "Przesuniecie canvy w górę - uzupełnienie z dołu"
            self.canva = np.vstack((self.canva, np.zeros((y_f + h_f - w_c, h_c, 3), np.uint8)))
            self.alpha = np.vstack((self.alpha, np.zeros((y_f + h_f - w_c, h_c, 1), np.uint16)))

        w_c, h_c, _ = self.canva.shape
        if y_f < 0:
            "Przesuniecie canvy w dół - uzupełnienie z góry"
            self.canva = np.vstack((np.zeros((-y_f, h_c, 3), np.uint8), self.canva))
            self.alpha = np.vstack((np.zeros((-y_f, h_c, 1), np.uint16), self.alpha))
            self.y -= y_f  # ~0
            y_r = self.roi[1]
            y_f = 0

        # wypełenie klatki
        l = x_f
        r = x_f + w_f
        t = y_f
        b = y_f + h_f
        lvl = (self.alpha[t:b, l:r]) == 0
        self.canva[t:b, l:r] = self.canva[t:b, l:r] * (1 - lvl) + lvl * frame

        # obliczenie wspolczynnika, zsumowanie roi i canvy
        l = x_r
        r = x_r + w_r
        t = y_r
        b = y_r + h_r
        lvl = 1 / (self.alpha[t:b, l:r] + 1)
        self.canva[t:b, l:r] = self.canva[t:b, l:r] * (1 - lvl) + lvl * roi
        self.alpha[t:b, l:r] += 1

        # pobieranie pełnej klatki z canvy
        l = x_f
        r = x_f + w_f
        t = y_f
        b = w_f + h_f
        return self.canva[t:b, l:r]
        # return self.alpha / 255
