# -*- coding: utf-8 -*-
"""
ita.py
=================
Implementation of the Innovative Trend Analysis method proposed by Zekai Sen (2011).
Innovative Trend Analysis is a graphical method to examine the trends in time
series data. Sequential Mann-Kendall test uses the intersection of prograde and
retrograde series to indicate the possible change point in time series data.
Distribution free cumulative sum charts indicate location and significance of
the change point in time series.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import stats
from statsmodels.stats.weightstats import ztest

from src.definitions import RESULTS_DIR
from src.methods.method import Method
from src.utils import generate_timestamp


class ITA(Method):
    def __init__(self, confidence: float = 0.95, plot: bool = False, save_name: str = 'ita_result',
                 save_path: str = RESULTS_DIR + '/', save_format: str = 'png', file_id: str = None):
        """
        Instantiation method of the innovative trend analysis.

        :param plot: flag to plot the result in the screen, false by default
        :param save_name: set the name of the file that contains the result
        :param save_path: set the path where the result will be saved
        :param save_format: set the file format of the result
        :param file_id: parameter to set an special id to the generated file
        """
        super().__init__('ITA')
        self.confidence_level = 1 - confidence
        self.plot = plot
        self.save_path = save_path
        self.save_format = save_format
        self.save_name = save_name
        self.file_id = file_id

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """
        Method that performs the Innovative Trend Analysis to the given time-series
        or signal. This method is visual so the result will be the creation of a
        file with the plot of the result.

        :param time_series_x: time variable of the time series to analyze
        :param time_series_y: value of the time series to analyze
        """
        # Odd time series are problematic
        if time_series_y.shape[0] // 2 !=0:
            time_series_y = time_series_y[:-1]
        first_half, second_half = np.split(time_series_y, indices_or_sections=2)
        first_half = np.sort(first_half)
        second_half = np.sort(second_half)

        self._plot_ita(first_half=first_half, second_half=second_half,
                       time_series_min=np.min(time_series_y),
                       time_series_max=np.max(time_series_y))

        second_half = second_half - first_half
        np.random.shuffle(second_half)

        # comparing with no trend line mean
        if second_half.shape[0] < 30:
            _, p_score = stats.ttest_1samp(second_half, 0.0)
        else:
            _, p_score = ztest(second_half, value=0.0)

        trend = p_score <= self.confidence_level
        return trend,

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """ Not valid for ITA """
        raise NotImplementedError('This method does not have the capability of estimating a trend')

    def _plot_ita(self, first_half: np.ndarray, second_half: np.ndarray,
                  time_series_min, time_series_max):
        """
        Plotting of the Innovative Trend Analysis results.

        It generates a plot that is saved as png in the folder 'results/ita/'.
        If the flag 'plot' is True, the plot will be shown in the screen apart
        of being saved in the folder.

        :param first_half: first half of the time series values
        :param second_half: second half of the time series values
        :param time_series_min: minimum value of the time series
        :param time_series_max: maximum value of the time series
        """
        plt.figure()
        plt.scatter(first_half, second_half, label='data', color='red', s=2)
        plt.title('Innovative Trend Analysis')
        plt.xlabel('First half of the series')
        plt.xlim(time_series_min, time_series_max)
        plt.ylabel('Second half of the series')
        plt.ylim(time_series_min, time_series_max)
        # No trend line
        x_no_trend = np.array([time_series_min, time_series_max])
        y_no_trend = 0 + 1 * x_no_trend
        plt.plot(x_no_trend, y_no_trend, label='(1:1) No trend line',
                 color='black', linewidth=0.75, linestyle='-')
        plt.legend()
        # Save file with timestamp of the execution
        timestamp = generate_timestamp()
        if self.file_id is not None:
            file_id = "{0}_{1}".format(self.file_id, timestamp)
        else:
            file_id = timestamp
        plt.savefig("{0}/{1}_{2}.{3}".format(self.save_path, self.save_name, file_id, self.save_format))
        if self.plot:
            plt.show()
        plt.close()
