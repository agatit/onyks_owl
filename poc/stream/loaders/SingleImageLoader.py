import cv2

from stream.loaders.Loader import Loader


class SingleImageLoader(Loader):
    def get_image_gen(self):
        str_input_path = str(self.input_path)
        yield cv2.imread(str_input_path)
