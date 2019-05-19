# -*- coding: utf-8 -*-
"""
method.py
=================
Abstract class that all the methods will import in order to have a generalized
structure. Every method will implement their specific functionality.
"""
import abc

import numpy as np
from scipy import stats


class Method(abc.ABC):

    @abc.abstractmethod
    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Function used to execute the trend detection process of the method.

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: method specific data about the trend in the time series
        """
        raise NotImplementedError('This method does not have the capability of detecting a trend')

    @abc.abstractmethod
    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Function used to execute the trend estimation process of the method

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: array with the trend data
        """
        raise NotImplementedError('This method does not have the capability of estimating a trend')

    @staticmethod
    def describe_trend_from_array(x_time_series: np.ndarray, trend: np.ndarray):
        """
        Method that analyze the trend and by fitting a linear regression on it estimates
        the type of trend is, if it is really a trend.

        The function `linregress()` returns the information about the regression fitted
        like the slope and the intercept. It also returns the p value whose null hypothesis
        is that the slope is zero.

        Therefore, If we observe a large p-value, for example larger than 0.05 or 0.1,
        then we cannot reject the null hypothesis of identical average scores.
        If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we reject
        the null hypothesis of equal averages.

        :param x_time_series: time variable of the time series
        :param trend: array with the values of the identified trend
        :return: True if the trend detected by the method is really a trend, False otherwise
        and the type of trend: 'Increasing', 'Decreasing' and 'No trend'
        """
        if trend is not None:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_time_series, trend)
            if p_value < 0.05:  # There is a significant trend, not 0 mean
                if slope > 0.:
                    return True, 'Increasing'
                elif slope < 0.:
                    return True, 'Decreasing'
        return False, 'No trend'
