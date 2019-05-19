import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from src.methods.method import Method


class Regression(Method):

    def __init__(self, order: int = 5):
        self.order = order

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        self.describe_trend_from_array(time_series_x, trend)

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        data_complete = []
        for i in range((self.order + 1)):
            data_complete.append(time_series_x ** i)
        data_complete = np.array(data_complete).T
        model = LinearRegression().fit(data_complete, time_series_y)
        return model.predict(data_complete)

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        super().visualize_trend(time_series_x, time_series_y, 'Linear Regression')