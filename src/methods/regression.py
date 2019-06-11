import numpy as np
from sklearn.linear_model import ElasticNet

from src.methods.method import Method


class Regression(Method):

    def __init__(self, order: int = 5):
        super().__init__('Regression')
        self.order = order

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        return self.describe_trend_from_array(time_series_x, trend)

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):

        x = np.copy(time_series_x)
        y = np.copy(time_series_y)

        x = np.linspace(0, len(x), len(x))

        # To avoid 0-division errors
        ts_min = np.min(y)
        y += -ts_min

        data_complete = []

        # Polynomial comps
        for i in range((self.order + 1)):
            data_complete.append(x ** i)
            data_complete.append((x + 1) ** -i)
            data_complete.append(x ** (1 / (i + 1)))

        # Log
        data_complete.append(np.log1p(x))

        # Exp
        data_complete.append(2 ** x)
        data_complete.append(3 ** x)

        # Some sinusoids based on series length
        for i in np.arange(1, 3, 0.1):
            data_complete.append(np.sin(x * (np.pi) / (len(x) / 2)))

        data_complete = np.array(data_complete).T
        model = ElasticNet().fit(data_complete, y)

        return model.predict(data_complete) + ts_min

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        super().visualize_trend(time_series_x, time_series_y, 'Least squares', 'Estimated trend')
