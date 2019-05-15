#%%

from src.data_handler.data_handler import generate_synthetic_data
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter


x, y, trend, seasonality, noise = generate_synthetic_data('function', 'data.ini')

methods = [EmpiricalModeDecomposition(), HPfilter()]

for method in methods:
    method.visualize_trend(x,y)

