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
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
from patsy import dmatrix
# from math import sqrt
from src.methods.method import Method

# x = np.arange(0, 100)
# y = np.arange(0, 100)
# noise = np.random.normal(size=100)
# signal = y + noise
#
# time_series_x = signal
# time_series_y = y


class Splines(Method):

    def __init__(self, knots: Tuple = (20,40,60,80), degree: int = 3):
        """
        :param

        """
        self.degree = degree
        self.knots = knots


    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):

        # train_x, valid_x, train_y, valid_y = train_test_split(time_series_x, time_series_y, test_size = 0.33, random_state=1)

        # Cubic spline generation (4 knots)
        reshaped_x = dmatrix(f"bs(time_series, knots={self.knots}, degree = {self.degree}, include_intercept=False)",
                             {"time_series": time_series_x}, return_type='dataframe')

        # Fitting Generalised linear model on transformed dataset
        reg_fitting = sm.GLM(time_series_y, reshaped_x).fit()

        # Prediction on splines
        trend = reg_fitting.predict(
            dmatrix(f"bs(time_series, knots={self.knots}, degree = {self.degree}, include_intercept=False)",
                    {"time_series": time_series_x},return_type='dataframe'))

        return trend

# Generating natural cubic spline
# transformed_x3 = dmatrix("cr(train,df = 3)", {"train": train_x}, return_type='dataframe')

# fit3 = sm.GLM(train_y, transformed_x3).fit()

# Prediction on validation set
# pred3 = fit3.predict(dmatrix("cr(valid, df=3)", {"valid": valid_x}, return_type='dataframe'))

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method does not have the capability of detecting a trend')

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        # print(trend.shape)
        # Plot the splines and error bands
        # plt.scatter(time_series_x,x time_series_y, facecolor='None', edgecolor='k', alpha=0.1)
        plt.plot(time_series_x, trend, color='r', label=f'Specifying degree = {self.degree} with {self.knots} knots')
        plt.legend()

        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.title('Spline Regression')
        plt.show()

# plt.plot(time_series_x, pred3,color='g', label='Natural spline')
# plt.xlim(15,85)
# plt.ylim(0,350)
