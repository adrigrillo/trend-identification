import numpy as np
from sklearn.linear_model import LinearRegression
from method import Method

x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)


class regression(Method):

    def detect_trend(self, time_series: np.ndarray, y, order):
        data_complete = []
        for i in range((order + 1)):
            data_complete.append(time_series ** i)
        data_complete = np.array(data_complete).T
        model = LinearRegression().fit(data_complete, y)
        return model


m = regression().detect_trend(x, y, 1)
print(m.coef_)
