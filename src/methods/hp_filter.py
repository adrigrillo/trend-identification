# -*- coding: utf-8 -*-
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

import numpy as np
import statsmodels.api as sm

from src.methods.method import Method


class HPfilter(Method):

    def __init__(self, smoothing: int = 1600):
        """
        Instantiation of the Hodrick-Prescott method.

        :param smoothing: Hodrick-Prescott smoothing parameter. It is suggested to use a
        value of 1600 for quarterly data, 6.25 (1600/4**4) for annual data and
        129600 (1600*3**4) for monthly data.
        """
        self.smoothing = smoothing

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method does not have the capability of detecting a trend')

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Function used to execute the trend estimation process of the method

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: the estimated cycle and trend data
        """
        cycle, trend = sm.tsa.filters.hpfilter(time_series_y, 1600)
        return cycle, trend
