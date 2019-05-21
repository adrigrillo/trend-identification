from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

import numpy as np
import sys
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from scipy.optimize import brute
from src.methods.method import Method
import numpy.random as random
from sklearn.model_selection import ParameterGrid

x = np.linspace(0, 100, num=100)
trend = x + 25 * np.sin(x/6)
y = x + 25 * np.sin(x/6) + 12 * random.randn(len(x))
# y = np.sin(y)

# plt.plot(y)
# plt.plot(trend)
# plt.show()

class Arima(Method):

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        pass

    def detect_trend(self, time_series: np.ndarray, y):
        # series = np.concatenate((x.reshape(len(x),1),y.reshape(len(y),1)),axis=1)
        x = time_series

        #
        #   <auto.arima> Automatic Time Series Forecasting: The forecast Package for R, Hyndman & Khandakar, 2008
        #

        # Bounds for the auto.arima constraints
        pq_bound = 5
        PQ_bound = 2

        param_grid = list(ParameterGrid({'m':range(2,30,3), 'd':range(3), 'D':range(3)}))

        # Create function for searching the variation
        def objfunc(order):
            try:
                order, sorder = order[:3], order[3:]
                fit = SARIMAX(y,x, order, sorder).fit(disp=False)
                # Return AIC, ignoring nans as invalid models are not good fits
                return fit.aic if (not np.isnan(fit.aic)) else sys.float_info.max
            except Exception as e:
                # Ignore exceptions, they are likely poor fits.
                return sys.float_info.max

        grid_order = (0,0,0,0,0,0,0)
        grid_aic = sys.float_info.max

        for params in param_grid:

            d = params['d']
            D = params['D']
            m = params['m']

            print(d,D,m)

            # Step 1
            initial_models = [
                (2,d,2,1,D,1,m),
                (0,d,0,0,D,0,m),
                (1,d,0,1,D,0,m),
                (0,d,1,0,D,1,m)
            ]

            aics = list(map(lambda x: objfunc(x), initial_models))
            current_aic = np.min(aics)
            best_aic_index = np.argmin(aics)
            (p, d, q, P, D, Q, m) = initial_models[best_aic_index]

            # Step 2

            model_found = False
            while not model_found:
                # Create the order sets
                orders = [
                    # p,q,P,D can each vary by +-1
                    (p-1,d,q,P,D,Q,m),
                    (p,d,q-1,P,D,Q,m),
                    (p,d,q,P-1,D,Q,m),
                    (p,d,q,P,D,Q-1,m),
                    (p+1,d,q,P,D,Q,m),
                    (p,d,q+1,P,D,Q,m),
                    (p,d,q,P+1,D,Q,m),
                    (p,d,q,P,D,Q+1,m),
                    # p,q or P,Q may vary in combination by +-1
                    (p-1,d,q-1,P,D,Q,m),
                    (p+1,d,q+1,P,D,Q,m),
                    (p,d,q,P-1,D,Q-1,m),
                    (p,d,q,P+1,D,Q+1,m),
                ]

                # Prune options based on constraints
                orders = list(filter(lambda x: x[0] <= pq_bound and x[2] <= pq_bound and x[3] <= PQ_bound and x[5] <= PQ_bound, orders))
                # Negative orders are not sensible
                orders = list(filter(lambda x: x[0] >= 0 and x[2] >= 0 and x[3] >= 0 and x[5] >= 0, orders))
                # Roots of psis & thetas constraint?

                # Evaluate the models and choose lowest AIC
                model_aics = list(map(lambda x: objfunc(x), orders))
                min_aic = np.min(model_aics)
                min_order_index = np.argmin(model_aics, axis=0)
                min_order = orders[min_order_index]

                # If we can't find a better AIC, we're done
                if min_aic > current_aic:
                    model_found = True
                else:
                    (p, d, q, P, D, Q, m) = min_order
                    current_order = min_order
                    current_aic = min_aic

            # At this point, we have best models for these d,D and m.
            if current_aic < grid_aic:
                grid_aic = current_aic
                grid_order = current_order
            print('Current best: ', grid_order, ' aic: ', grid_aic)


        #
        #   </auto.arima>
        #

        print('Opt params: ', grid_order)
        print('Resulting aic: ', grid_aic)

        # Rebuild the model with optimal params
        model = SARIMAX(y, x, grid_order[:3], grid_order[3:])
        model_fit = model.fit(disp=False)


        return model_fit, grid_order, model


m_fit, opt_order, model = Arima().detect_trend(x, y)

print(m_fit.summary())
print('Parameters: ', m_fit.params)
pred = m_fit.predict(start=45, end=99)

print(np.sum(np.abs((y[45:] - pred) - trend[45:])))

plt.plot()

plt.plot(y)
plt.plot(pred)
plt.plot(trend)
plt.show()