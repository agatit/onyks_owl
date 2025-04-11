import numpy as np

from rectify_optimalization.full_config_objective_functions.FullConfigObjectiveFunction import FullConfigObjectiveFunction


class MeanFullConfigObjectiveFunction(FullConfigObjectiveFunction):
    def _aggregate_method(self, method_result: np.ndarray) -> float:
        # return method_result.mean(axis=1).sum()
        return method_result.mean().sum()
