import numpy as np
from scipy import stats
from src.methods.method import Method


x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)


class Theil(Method):

    def __init__(self,confidence: float=0.9):
        self.confidence=confidence

    def detect_trend(self, time_series_x: np.ndarray,time_series_y: np.ndarray):
        return stats.theilslopes(time_series_y, time_series_x, self.confidence)

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method does not have the capability of estimating a trend')


#m = theil().detect_trend(x, y)
#print(m)
