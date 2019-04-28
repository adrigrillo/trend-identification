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

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from src.methods.method import Method


class ITA(Method):
    def __init__(self, save_name: str = 'ita_result',
                 save_path: str = '../../results/ita',
                 save_format: str = 'png'):
        """
        Instantiation method of the innovative trend analysis.

        :param save_name: set the name of the file that contains the result
        :param save_path: set the path where the result will be saved
        :param save_format: set the file format of the result
        """
        self.save_path = save_path
        self.save_format = save_format
        self.save_name = 'ita_result'

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray,
                     plot: bool = False, file_id: str = None):
        """
        Method that performs the Innovative Trend Analysis to the given time-series
        or signal. This method is visual so the result will be the creation of a
        file with the plot of the result.

        :param time_series_x: time variable of the time series to analyze
        :param time_series_y: value of the time series to analyze
        :param plot: flag to plot the result, false by default
        :param file_id: parameter to set an special id to the generated file
        """
        first_half, second_half = np.split(time_series_y, indices_or_sections=2)
        first_half = np.sort(first_half)
        second_half = np.sort(second_half)

        # TODO: implement a numeric method

        self._plot_ita(file_id=file_id,
                       plot=plot,
                       first_half=first_half,
                       second_half=second_half,
                       time_series_min=np.min(time_series_x),
                       time_series_max=np.max(time_series_x))

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        """ Not valid for ITA """
        raise NotImplementedError('This method does not have the capability of estimating a trend')

    def _plot_ita(self, first_half: np.ndarray, second_half: np.ndarray,
                  time_series_min, time_series_max, plot: bool = False,
                  file_id: str = None):
        """
        Plotting of the Innovative Trend Analysis results.

        It generates a plot that is saved as png in the folder 'results/ita/'.
        If the flag 'plot' is True, the plot will be shown in the screen apart
        of being saved in the folder.

        :param first_half: first half of the time series values
        :param second_half: second half of the time series values
        :param time_series_min: minimum value of the time series
        :param time_series_max: maximum value of the time series
        :param plot: flag to plot the result, false by default
        :param file_id: parameter to set an special id to the generated file
        """
        plt.plot(first_half, second_half, label='data', color='red',
                 linewidth='3', linestyle='dotted')
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
        time = datetime.now()
        timestamp = '{0}-{1}-{2}'.format(str(time.hour), str(time.minute), str(time.second))
        if file_id is not None:
            file_id = "{0}_{1}".format(file_id, timestamp)
        else:
            file_id = timestamp
        plt.savefig("{0}/{1}_{2}.{3}".format(self.save_path, self.save_name, file_id, self.save_format))
        if plot:
            plt.show()
