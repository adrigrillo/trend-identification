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

from datetime import datetime
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

    def detect_trend(self, time_series: np.ndarray, plot: bool = False,
                     file_id: str = None) -> None:
        """
        Method that performs the Innovative Trend Analysis to the given time-series
        or signal. This method is visual so the result will be the creation of a
        file with the plot of the result.

        :param time_series: the time series to analyze.
        :param plot: flag to plot the result, false by default.
        :param file_id: parameter to set an special id to the generated file
        """
        first_half, second_half = np.split(time_series, indices_or_sections=2)
        first_half = np.sort(first_half)
        second_half = np.sort(second_half)
        plt.plot(first_half, second_half, label='data', color='red',
                 linewidth='3', linestyle='dotted')
        plt.title('Innovative Trend Analysis')
        plt.xlabel('First half of the series')
        plt.xlim(np.min(time_series), np.max(time_series))
        plt.ylabel('Second half of the series')
        plt.ylim(np.min(time_series), np.max(time_series))
        # No trend line
        axes = plt.gca()
        x_no_trend = np.array(axes.get_xlim())
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
