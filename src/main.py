#%%
import os.path
import numpy as np
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.arima import Arima
from src.methods.ita import ITA
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.splines import Splines
from src.methods.theil import Theil
from src.methods.dws import DWS
from src.data_handler import data_handler

methods_detection = [ITA(), MannKendall(), Regression(), Theil()]
methods_estimation = [DWS(), EmpiricalModeDecomposition(), HPfilter(), Regression(), Splines()]


x_values, y_values, trend_values, seasonality_values, noise_values = data_handler.generate_synthetic_data('function', 'data.ini')
methods = [Splines()]


# path = '/data/generated_data'
# num_files = len([f for f in os.listdir(path)
#                 if os.path.isfile(os.path.join(path, f))]) - 1
# xs = np.zeros(num_files)
# ys = np.zeros(num_files)

#for i in num_files:

#for method in methods_detection:
#    method.detect_trend(x, y)


for method in methods:
   method.visualize_trend(x_values, y_values)










