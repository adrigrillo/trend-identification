import configparser

import numpy as np
import pandas as pd

from src.definitions import SYNTHETIC_DIR, GENERATED_DIR
from src.methods.dws import DWS
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.ita import ITA
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.splines import Splines
from src.methods.theil import Theil

methods_detection = [MannKendall(), ITA(), Regression(), Theil(), DWS(),
                     EmpiricalModeDecomposition(), HPfilter(), Regression(),
                     Splines()]

### DETECTION:
table = np.zeros((len(methods_detection), 5))
for i in range(5):
    name = '/func_' + str(i + 1)
    data = pd.read_csv(GENERATED_DIR + name + '.csv')
    config_file_path = SYNTHETIC_DIR + name + '.ini'
    params = configparser.ConfigParser(allow_no_value=True)
    params.read(config_file_path)
    x, y, trend, seasonality, noise = \
        data.x.to_numpy(), data.y.to_numpy(), data.trend.to_numpy(), data.seasonality.to_numpy(), data.noise.to_numpy()
    for j in range(len(methods_detection)):
        detect_trend = methods_detection[j].detect_trend(x, y)
        table[j][i] = detect_trend[0]

print(table)
