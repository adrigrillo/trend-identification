import numpy as np
from scipy import stats
from method import Method


x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)


class theil(Method):

    def detect_trend(self, time_series: np.ndarray,y, confidence):
        return stats.theilslopes(y, x, confidence)


m = theil().detect_trend(x, y, 0.9)
print(m)
