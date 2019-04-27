# -*- coding: utf-8 -*-
"""
method.py
=================
Abstract class that all the methods will import in order to have a generalized
structure. Every method will implement their specific functionality.
"""
import abc

import numpy as np


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
        :return: method specific data about the trend in the time series
        """
        raise NotImplementedError('This method does not have the capability of estimating a trend')
