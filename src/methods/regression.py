import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from src.methods.method import Method

x = np.linspace(0, 500, num=100)
y = np.linspace(0, 500, num=100)


class Regression(Method):

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
        return model.predict(data_complete)

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)

<<<<<<< HEAD
m = regression().detect_trend(x, y)
print(m.shape)
=======
        plt.plot(trend)
        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.title('Linear Regression')
        plt.show()


#m = regression().detect_trend(x, y)
#print(m.coef_)
>>>>>>> 84ab8d505a3145ec88003f32c08cd1b6fb2928ae
