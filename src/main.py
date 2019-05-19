#%%
import os.path
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import configparser

from src.definitions import *
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.arima import Arima
from src.methods.ita import ITA
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.theil import Theil
from src.methods.dws import DWS
from src.data_handler import data_handler
from src.data_handler.data_generator import generate_data

#methods_detection = [ITA(), MannKendall(), Regression(), Theil()]
methods_estimation = [EmpiricalModeDecomposition(), HPfilter(), Regression()]


#x_values, y_values, trend_values, seasonality_values, noise_values = data_handler.generate_synthetic_data('function', 'time_series_2.ini')
#method = EmpiricalModeDecomposition()

# Estimate trends on generated data and save plots
num_files = len([f for f in os.listdir(GENERATED_DIR)
               if os.path.isfile(os.path.join(GENERATED_DIR, f))]) - 1
for i in range(1, num_files + 1):
    name = '/time_series_' + str(i)
    data = pd.read_csv(GENERATED_DIR + name + '.csv')
    config_file_path = SYNTHETIC_DIR + name + '.ini'
    params = configparser.ConfigParser(allow_no_value=True)
    params.read(config_file_path)
    x, y, trend, seasonality, noise = \
        data.x.to_numpy(), data.y.to_numpy(), data.trend.to_numpy(), data.seasonality.to_numpy(), data.noise.to_numpy()
    plt.figure()
    plt.plot(x, y, label='true trend')
    plt.title(f'trend: {params[TREND_DATA][FUNC]}, '
              f'seasonality: {params[SEASONALITY_DATA][FUNC]}, '
              f'snr: {params[NOISE_DATA][SIGNAL_TO_NOISE]}')
    for method in methods_estimation:
        plt.plot(x, method.estimate_trend(x, y), label=type(method).__name__)
    plt.legend()
    plt.savefig(PLOTS_DIR + name + '.png')
    plt.close()


#for method in methods_detection:
#    method.detect_trend(x, y)











