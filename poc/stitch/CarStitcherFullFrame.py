import numpy as np


class CarStitcherFullFrame:
    def __init__(self):

        self.x_pos = 0  # pozycja ostatniej ramki względem canvy
        self.y_pos = 0

        self.canva = None
        self.alpha = None

    def next(self, frame, velocity):
        velocity_x, velocity_y = velocity
        y_1, x_1, _ = frame.shape

        if self.canva is None or velocity == (0, 0):
            "przypisanie pierwszej klatki do canvy"
            self.canva = frame
            self.alpha = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint16)
            return frame

        self.x_pos -= velocity_x
        self.y_pos -= velocity_y
        x_pos = int(self.x_pos)  # zaokrąglenie w kierunku 0
        y_pos = int(self.y_pos)

        # rozszerzanie canvy i alphy do odpowiedniego polozenia zdjecia
        y_c, x_c, _ = self.canva.shape
        if x_pos + x_1 > x_c:
            "Przesuniecie canvy w lewo - uzupełninie z prawej"
            self.canva = np.hstack((self.canva, np.zeros((y_c, x_pos + x_1 - x_c, 3), np.uint8)))
            self.alpha = np.hstack((self.alpha, np.zeros((y_c, x_pos + x_1 - x_c, 1), np.uint16)))

        y_c, x_c, _ = self.canva.shape
        if x_pos < 0:
            "Przesuniecie canvy w prawo - uzupełnienie z lewej, korekta ofsetu"
            self.canva = np.hstack((np.zeros((y_c, -x_pos, 3), np.uint8), self.canva))
            self.alpha = np.hstack((np.zeros((y_c, -x_pos, 1), np.uint16), self.alpha))
            self.x_pos -= x_pos  # ~0
            x_pos = 0

        # uzupełnianie pionu
        y_c, x_c, _ = self.canva.shape
        if y_pos + y_1 > y_c:
            "Przesuniecie canvy w górę - uzupełnienie z dołu"
            self.canva = np.vstack((self.canva, np.zeros((y_pos + y_1 - y_c, x_c, 3), np.uint8)))
            self.alpha = np.vstack((self.alpha, np.zeros((y_pos + y_1 - y_c, x_c, 1), np.uint16)))

        y_c, x_c, _ = self.canva.shape
        if y_pos < 0:
            "Przesuniecie canvy w dół - uzupełnienie z góry"
            self.canva = np.vstack((np.zeros((-y_pos, x_c, 3), np.uint8), self.canva))
            self.alpha = np.vstack((np.zeros((-y_pos, x_c, 1), np.uint16), self.alpha))
            self.y_pos -= y_pos  # ~0
            y_pos = 0

        # obliczenie wspolczynnika, zsumowanie klatki i canvy, i inkrementacja wartosci self.alpha
        l = x_pos
        r = x_pos + x_1
        t = y_pos
        b = y_pos + y_1

        lvl = 1 / (self.alpha[t:b, l:r] + 1)
        self.canva[t:b, l:r] = self.canva[t:b, l:r] * (1 - lvl) + lvl * frame
        self.alpha[t:b, l:r] += 1

        # ograniczenie ilości sumowanych klatek - nie działa :(
        # m = np.amax(self.alpha)
        # if m > 10:
        #     self.alpha -= m - 10

        return self.canva[t:b, l:r]
        # return self.alpha / 255
