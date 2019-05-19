"""
splines.py
=================

Source: https://www.analyticsvidhya.com/blog/2018/03/introduction-regression-splines-python-codes/

Spline regression is a semiparametric method since it has features of both - parametric and
nonparametric methods. It uses linear and polynomial regression techniques, which are parametric
methods but it doesn't assume any specific form of the curve. Regression splines are non-linear
regression techniques that divide the dataset into separate portions and fit the linear or
polynomial functions, called piecewise functions. These functions are connected by knots - the
join points where each of the segments are linked.

=================

Parameters:

    Number of knots

"""
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from patsy.highlevel import dmatrix

from src.methods.method import Method


class Splines(Method):

    def __init__(self, knots: Tuple = (20, 40, 60, 80), degree: int = 3):
        """
        :param knots: points of division of the series
        :param degree: degree of the polynomial in the regression
        """
        self.degree = degree
        self.knots = knots

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Cubic spline generation (4 knots)
        reshaped_x = dmatrix(f"bs(time_series, knots={self.knots}, degree = {self.degree}, include_intercept=False)",
                             {"time_series": time_series_x}, return_type='dataframe')
        # Fitting Generalised linear model on transformed dataset
        reg_fitting = sm.GLM(time_series_y, reshaped_x).fit()
        # Prediction on splines
        trend = reg_fitting.predict(reshaped_x)
        return trend.to_numpy()

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        return self.describe_trend_from_array(time_series_x, trend)

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        plt.plot(time_series_x, time_series_y, color='b', label=f'Original data')
        plt.plot(time_series_x, trend, color='r', label=f'Specifying degree = {self.degree} with {self.knots} knots')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Spline Regression')
        plt.show()
