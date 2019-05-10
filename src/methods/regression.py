import numpy as np
from sklearn.linear_model import LinearRegression
from method import Method

x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)


class regression(Method):

    def __init__(self,order: int=5):
        self.order=5

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        return self.estimate_trend(time_series_x,time_series_y)

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        data_complete = []
        for i in range((self.order + 1)):
            data_complete.append(time_series_x ** i)
        data_complete = np.array(data_complete).T
        model = LinearRegression().fit(data_complete, time_series_y)
        return model.coef_


m = regression().detect_trend(x, y)
print(m.coef_)
