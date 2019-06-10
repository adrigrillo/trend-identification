from sys import platform as sys_pf

if sys_pf == 'darwin':
    import matplotlib

    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

import numpy as np
import sys
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.methods.method import Method
import numpy.random as random
from sklearn.model_selection import ParameterGrid
import pmdarima as pm
import matplotlib.pyplot as plt


class Arima(Method):

    def __init__(self, seasonality: int = 1,
                 trace: bool = False, suppress_warnings: bool = True,
                 error_action: str = 'warn'):
        """
        Auto ARIMA initializer

        :param seasonality: The period for seasonal differencing, m refers to the number of periods
        in each season. For example, m is 4 for quarterly data, 12 for monthly data, or 1 for annual
        (non-seasonal) data. Default is 1. Note that if m == 1 (i.e., is non-seasonal),
        seasonal will be set to False.
        :param trace: whether to print status on the fits. Note that this can be very verbose.
        :param suppress_warnings: many warnings might be thrown inside of statsmodels.
        If suppress_warnings is True, all of the warnings coming from ARIMA will be squelched.
        :param error_action: If unable to fit an ARIMA due to stationarity issues, whether to warn (‘warn’),
        raise the ValueError (‘raise’) or ignore (‘ignore’). Note that the default behavior is to warn,
        and fits that fail will be returned as None. This is the recommended behavior, as statsmodels
        ARIMA and SARIMAX models hit bugs periodically that can cause an otherwise healthy parameter
        combination to fail for reasons not related to pmdarima.
        """
        self.seasonality = seasonality
        self.trace = trace
        self.suppress_warnings = suppress_warnings
        self.error_action = error_action

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        arima_fit = pm.auto_arima(time_series_y,
                                  m=self.seasonality,
                                  trace=self.trace,
                                  error_action=self.error_action,
                                  suppress_warnings=self.suppress_warnings)
        return arima_fit

    def detect_trend(self, time_series: np.ndarray, y):
        # series = np.concatenate((x.reshape(len(x),1),y.reshape(len(y),1)),axis=1)
        x = time_series

        #
        #   <auto.arima> Automatic Time Series Forecasting: The forecast Package for R, Hyndman & Khandakar, 2008
        #

        # Bounds for the auto.arima constraints
        pq_bound = 5
        PQ_bound = 2

        param_grid = list(ParameterGrid({'m': range(2, 30, 3), 'd': range(3), 'D': range(3)}))

        # Create function for searching the variation
        def objfunc(order):
            try:
                order, sorder = order[:3], order[3:]
                fit = SARIMAX(y, x, order, sorder).fit(disp=False)
                # Return AIC, ignoring nans as invalid models are not good fits
                return fit.aic if (not np.isnan(fit.aic)) else sys.float_info.max
            except Exception as e:
                # Ignore exceptions, they are likely poor fits.
                return sys.float_info.max

        grid_order = (0, 0, 0, 0, 0, 0, 0)
        grid_aic = sys.float_info.max

        for params in param_grid:

            d = params['d']
            D = params['D']
            m = params['m']

            print(d, D, m)

            # Step 1
            initial_models = [
                (2, d, 2, 1, D, 1, m),
                (0, d, 0, 0, D, 0, m),
                (1, d, 0, 1, D, 0, m),
                (0, d, 1, 0, D, 1, m)
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
                    (p - 1, d, q, P, D, Q, m),
                    (p, d, q - 1, P, D, Q, m),
                    (p, d, q, P - 1, D, Q, m),
                    (p, d, q, P, D, Q - 1, m),
                    (p + 1, d, q, P, D, Q, m),
                    (p, d, q + 1, P, D, Q, m),
                    (p, d, q, P + 1, D, Q, m),
                    (p, d, q, P, D, Q + 1, m),
                    # p,q or P,Q may vary in combination by +-1
                    (p - 1, d, q - 1, P, D, Q, m),
                    (p + 1, d, q + 1, P, D, Q, m),
                    (p, d, q, P - 1, D, Q - 1, m),
                    (p, d, q, P + 1, D, Q + 1, m),
                ]

                # Prune options based on constraints
                orders = list(
                    filter(lambda x: x[0] <= pq_bound and x[2] <= pq_bound and x[3] <= PQ_bound and x[5] <= PQ_bound,
                           orders))
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


if __name__ == '__main__':
    x = np.linspace(0, 100, num=100)
    trend = x + 25 * np.sin(x / 6)
    y = x + 25 * np.sin(x / 6) + 12 * random.randn(len(x))

    arima = Arima(seasonality=7)
    fit = arima.estimate_trend(x, y)

    plt.plot()

    plt.plot(y, label='Real')
    plt.plot(fit.predict(y.shape[0]), label='prediction')
    plt.legend()
    plt.show()
