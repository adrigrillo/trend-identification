
"""
hp_filter.py
=================
Hodrick–Prescott filter, is a method that decomposes a time series into a trend
(long-term) and a cyclical (short-term, recurring signal) component. HP filter
uses a smoothing parameter, lambda that can be tuned depending on what kind of
properties need to be captured. Smaller lambda captures the characteristics of
the short term signal and larger parameter captures the long-term component.

Source: https://www.statsmodels.org/dev/generated/statsmodels.tsa.filters.hp_filter.hpfilter.html

statsmodels.tsa.filters.hp_filter.hpfilter(X, lamb=1600)
[source code: https://www.statsmodels.org/dev/_modules/statsmodels/tsa/filters/hp_filter.html#hpfilter]
=================

Parameters:

X (array-like) – The 1d ndarray timeseries to filter of length (nobs,) or (nobs,1)

lamb (float) – The Hodrick-Prescott smoothing parameter. A value of 1600 is
suggested for quarterly data. Ravn and Uhlig suggest using a value of 6.25
(1600/4**4) for annual data and 129600 (1600*3**4) for monthly data.

Returns:

cycle (array) – The estimated cycle in the data given lamb.
trend (array) – The estimated trend in the data given lamb.
"""

import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

from src.methods.method import Method

x = np.arange(0, 100)
y = np.arange(0, 100)
noise = np.random.normal(size=100)
signal = y + noise

class HPfilter(Method):

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        pass

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):

        cycle, trend = sm.tsa.filters.hpfilter(time_series_y, 1600)

        plt.plot(time_series_y)
        plt.plot(trend)
        plt.plot(cycle)
        plt.show()

        return cycle, trend

estimation = HPfilter()
estimation.estimate_trend(signal, signal)
