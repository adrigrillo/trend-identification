import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from src.methods.method import Method


class Regression(Method):

    def __init__(self, order: int = 5):
        self.order = order

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method is not valid for detecting a trend')
    
    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        data_complete = []
        for i in range((self.order + 1)):
            data_complete.append(time_series_x ** i)
        data_complete = np.array(data_complete).T
        model = LinearRegression().fit(data_complete, time_series_y)
        return model.predict(data_complete)

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        plt.plot(time_series_y)
        plt.plot(trend)
        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.title('Linear Regression')
        plt.show()


if __name__ == '__main__':
    x = np.linspace(0, 500, num=100)
    y = np.linspace(0, 500, num=100)
    noise = np.random.normal(scale=50, size=100)
    reg = Regression()
    reg.visualize_trend(x, y + noise)
