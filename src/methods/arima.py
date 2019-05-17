import numpy as np
import sys
from statsmodels.tsa.arima_model import ARIMA
from scipy.optimize import brute
from src.methods.method import Method

x = np.linspace(0, 500, num=1000)
y = x + np.sin(x)
# y = np.sin(y)

opt_order = None


class Arima(Method):

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        pass

    def detect_trend(self, time_series: np.ndarray, y):
        # series = np.concatenate((x.reshape(len(x),1),y.reshape(len(y),1)),axis=1)
        x = time_series

        # Grid Search for ARIMA model (https://stackoverflow.com/questions/22770352/auto-arima-equivalent-for-python)

        # Redefine a func so order is first (used by brute)
        def objfunc(order, exog, endog):
            try:
                print('Fitting ARIMA with ', order)
                fit = ARIMA(endog, order, exog).fit(disp=False)
                # Return AIC, as we're evaluating based on that
                return fit.aic
            except Exception as e:
                # Ignore exceptions as they are from invalid configurations in the grid
                return sys.float_info.max
        # Create a grid (p,d,q)
        grid = (slice(0, 6, 1), slice(0, 5, 1), slice(0, 6, 1))

        # Apply
        # Brute returns the optimal args. If step size is changed, it needs to be accounted for in here
        opt_order = np.array(brute(objfunc, grid, args=(x, y), finish=None))

        print('Opt params: ', opt_order)

        # Rebuild the model with optimal params
        model_fit = ARIMA(y, opt_order.astype('int'), x).fit(disp=False)

        return model_fit


#m = Arima().detect_trend(x, y)
#print(m.predict(start=5,end=999)-y[5:])
