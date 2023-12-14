import numpy as np

from rectify_optimalization.objective_functions.ObjectiveFunction import ObjectiveFunction


class MeanObjectiveFunction(ObjectiveFunction):
    def _aggregate_method(self, method_result: np.ndarray) -> float:
        # return method_result.mean(axis=1).sum()
        return method_result.mean().sum()
