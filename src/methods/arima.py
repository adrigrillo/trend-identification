import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from method import Method

x = np.linspace(0, 500, num=1000)
y = np.linspace(0, 500, num=1000)

class arima(Method):

    def detect_trend(self, time_series: np.ndarray, y, p, d, q):
        # series = np.concatenate((x.reshape(len(x),1),y.reshape(len(y),1)),axis=1)
        x = time_series
        model = ARIMA(y, order=(p, d, q))
        model_fit = model.fit(disp=0)
        return model_fit


m = arima().detect_trend(x, y, 5, 1, 0)
print(m)
