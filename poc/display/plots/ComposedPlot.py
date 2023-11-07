from dataclasses import dataclass

from matplotlib import pyplot as plt


class ComposedPlot:
    def __init__(self, title, *axes_callback):
        self.title = title
        self.fig, self.ax1 = plt.subplots()

        self.axes = []
        for axe_callback in axes_callback:
            if len(self.axes) == 0:
                new_axe = self.ax1
            else:
                new_axe = self.ax1.twinx()

            axe_callback(new_axe)
            self.axes.append(new_axe)

        self.plots = []

    def add_plot(self, axe_index, x, y, **plot_params):
        axe = self.axes[axe_index]
        plot = axe.plot(x, y, **plot_params)
        self.plots.append(plot)

    def show_composed(self):
        self._init_plots()
        self.fig.show()

    def save_composed(self, output_path):
        self._init_plots()
        self.fig.savefig(output_path)

    def _init_plots(self):
        lines = [plot[0] for plot in self.plots]
        lines_labels = [line.get_label() for line in lines]
        self.ax1.legend(lines, lines_labels)
        self.ax1.set_title(self.title)