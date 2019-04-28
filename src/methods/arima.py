import numpy as np
from statsmodels.tsa.arima_model import ARIMA

from src.methods.method import Method

x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)


class Arima(Method):

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        pass

    def detect_trend(self, time_series: np.ndarray, y, p, d, q):
        # series = np.concatenate((x.reshape(len(x),1),y.reshape(len(y),1)),axis=1)
        x = time_series
        model = ARIMA(y, order=(p, d, q))
        model_fit = model.fit(disp=0)
        return model_fit


m = Arima().detect_trend(x, y, 5, 1, 0)
print(m)
