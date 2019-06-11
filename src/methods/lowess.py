import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess

from src.methods.method import Method


class Lowess(Method):
    def __init__(self):
        super().__init__('LOWESS')

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        pass

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Parametric search?
        estimate = lowess(time_series_y, time_series_x, return_sorted=False)

        return estimate

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        super().visualize_trend(time_series_x, time_series_y, 'Least squares', 'Estimated trend')
