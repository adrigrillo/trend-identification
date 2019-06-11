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

import numpy as np
import statsmodels.api as sm
from patsy.highlevel import dmatrix

from src.methods.method import Method


class Splines(Method):

    def __init__(self, quantile: Tuple = (0.25, 0.5, 0.75), degree: int = 3):
        """
        :param knots: points of division of the series
        :param degree: degree of the polynomial in the regression
        """
        super().__init__('Splines')
        self.quantile = quantile
        self.degree = degree

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Cubic spline generation (4 knots)
        # Durrleman and Simon (1989) recommends (0.05,0.50,0.95) for natural splines
        knots_array = np.quantile(time_series_x, self.quantile)
        knots = tuple(knots_array)
        reshaped_x = dmatrix(f"bs(time_series, knots = {knots}, degree = {self.degree}, include_intercept=False)",
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
        knots_array = np.quantile(time_series_x, self.quantile)
        knots = tuple(knots_array)
        super().visualize_trend(time_series_x, time_series_y, 'Spline Regression'
                                , f'Spline degree = {self.degree} with {knots} knots')
