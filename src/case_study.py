# %%
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from src.definitions import DATA_DIR, PLOTS_DIR
from src.methods.dws import DWS
from src.methods.hp_filter import HPfilter
from src.methods.ita import ITA
from src.methods.lowess import Lowess
from src.methods.method import Method
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.splines import Splines
from src.utils import generate_timestamp


def show_estimation(methods: List[Method], time_series_x: np.ndarray, time_series_y: np.ndarray) -> None:
    for method in methods:
        trend_estimation = method.estimate_trend(time_series_x, time_series_y)

        plt.figure(figsize=(12, 8))
        plt.plot(time_series_x, time_series_y)
        plt.plot(time_series_x, trend_estimation, label='Estimated trend')
        plt.title(f'Trend estimation of {method.name}')
        plt.xlabel('Days from January 1962 to July 2012')
        plt.ylabel('Difference between LOD and 86400 seconds (ms)')
        plt.savefig(f'{PLOTS_DIR}/case_study_{generate_timestamp()}.png')
        plt.show()
        plt.close()


if __name__ == '__main__':
    methods_detection = [MannKendall(), ITA(plot=True)]
    methods_estimation = [Regression(), Lowess(), Splines(), HPfilter(), DWS()]

    data = loadmat(f'{DATA_DIR}/case_study.mat')
    y = data['LOD'].squeeze()
    x = np.arange(0, y.shape[0])

    #print(method_detection.detect_trend(x, y))

    show_estimation(methods_estimation, x, y)
