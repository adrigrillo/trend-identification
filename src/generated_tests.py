# %%
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from src.compare_functions import trend_estimation_comparison, trend_detection_comparison
from src.data_handler import data_handler
from src.methods.dws import DWS
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.ita import ITA
from src.methods.lowess import Lowess
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.splines import Splines
from src.methods.theil import Theil

if __name__ == '__main__':
    methods_detection = [ITA(), MannKendall(), Regression(), Theil()]
    methods_estimation = [EmpiricalModeDecomposition(), HPfilter(), Splines(), Theil(), Regression(), Lowess()]

    trend_detection_comparison(methods_estimation, '*')
    trend_estimation_comparison(methods_estimation, '*')
