#%%
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.arima import Arima
from src.methods.ita import ITA
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.theil import Theil

methods_detection = [Arima(), ITA(), MannKendall(), Regression(), Theil()]
methods_estimation = [EmpiricalModeDecomposition(), HPfilter(), Regression()]


#for method in methods_detection:
#    method.detect_trend(x, y)

#for method in methods_estimation:
#    method.visualize_trend(x, y)









