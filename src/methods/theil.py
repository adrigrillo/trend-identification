from typing import Tuple

import numpy as np
from scipy import stats

from src.methods.method import Method


class Theil(Method):

    def __init__(self, confidence: float = 0.9):
        self.confidence = confidence

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Function used to execute the trend detection process of the method.

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: True if the trend detected by the method is really a trend, False otherwise
        and the type of trend: 'Increasing', 'Decreasing' and 'No trend'
        """
        trend = self.estimate_trend(time_series_x, time_series_y)
        return self.describe_trend_from_array(time_series_x, trend)

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray) -> np.ndarray:
        """
        Function used to execute the trend estimation process of the method

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: array with the trend
        """
        slope, intercept, lo_slope, hi_slope = stats.theilslopes(time_series_y,
                                                                 time_series_x,
                                                                 self.confidence)
        trend = intercept + slope * time_series_x
        return trend
