import ipywidgets as widgets
import pandas as pd


class RegressionMethodView:
    def __init__(self, name, run_on_df_callback):
        self.name = name
        self.run_on_df_callback = run_on_df_callback

        self.progress_bar = widgets.IntProgress()
        self.progress_bar.description = self.name

        self.output = []
        self.df = pd.DataFrame()

    def run(self):
        def wrapper(df_part):
            self.run_on_df_callback(df_part, self.output)
            self.progress_bar.value += 1

        return wrapper

    def reset_progress_bar(self):
        self.progress_bar.value = 0

    def reset_output(self):
        self.output = []
