from stitch.speed.RegressionModel import RegressionModel


class VelocityEstimator:
    def __init__(self, window_size, window_step):
        self.window_size = window_size
        self.window_step = window_step

        self.regression_model = RegressionModel()

        self.moved_frames_counter = 0

    def prepare_model(self, frames):
        pass

    def get_velocity(x):
        pass

    def update():
        pass
