# -*- coding: utf-8 -*-
"""
mk.py
=================
This function is derived from code originally posted by Sat Kumar Tomer
(satkumartomer@gmail.com)
See also: http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm

The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
1987) is to statistically assess if there is a monotonic upward or downward
trend of the variable of interest over time. A monotonic upward (downward)
trend means that the variable consistently increases (decreases) through
time, but the trend may or may not be linear. The MK test can be used in
place of a parametric linear regression analysis, which can be used to test
if the slope of the estimated linear regression line is different from
zero. The regression analysis requires that the residuals from the fitted
regression line be normally distributed; an assumption not required by the
MK test, that is, the MK test is a non-parametric (distribution-free) test.
Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
viewed as an exploratory analysis and is most appropriately used to
identify stations where changes are significant or of large magnitude and
to quantify these findings.
"""

import numpy as np
from scipy.stats import norm

from src.methods.method import Method


class MannKendall(Method):

    def __init__(self, alpha: float = 0.05):
        """
        Initialization method for Mann-Kendall
        
        :param alpha: significance level (0.05 default)
        """
        super().__init__('MK')
        self.alpha = alpha

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Method that performs the Mann-Kendall test to the given time-series
        or signal.

        :param time_series_x: time variable of the time series to analyze
        :param time_series_y: value of the time series to analyze
        :return: a tuple with: true if there is a trend or false otherwise, the
        trend type (increasing, decreasing or no trend), the p value of the
        significance test and normalized test statistics.
        """
        n = len(time_series_y)

        # calculate S
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(time_series_y[j] - time_series_y[k])

        # calculate the unique data
        unique_x = np.unique(time_series_y)
        g = len(unique_x)

        # calculate the var(s)
        if n == g:  # there is no tie
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:  # there are some ties in data
            tp = np.zeros(unique_x.shape)
            for i in range(len(unique_x)):
                tp[i] = sum(time_series_y == unique_x[i])
            var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:  # s == 0:
            z = 0

        # calculate the p_value
        p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
        trend_present = abs(z) > norm.ppf(1 - self.alpha / 2)

        if (z < 0) and trend_present:
            trend_type = 'decreasing'
        elif (z > 0) and trend_present:
            trend_type = 'increasing'
        else:
            trend_type = 'no trend'

        return trend_present, trend_type, p, z

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method does not have this function')
