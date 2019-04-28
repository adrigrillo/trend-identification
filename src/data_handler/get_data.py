import numpy as np
import pandas as pd

from src.data_handler import view

x = np.arange(0, view.number_of_data)
if view.gaussian:
    noise = np.random.normal(view.noise_mean, view.noise_deviation, view.number_of_data)
else:
    noise = np.random.rand(view.number_of_data)

x = eval(view.equation)

if view.seasonality:
    y = np.arange(0, view.number_of_data)
    # y = eval(view.equation_season)
    y = np.sin(y)
    data_processed = x + noise + y
else:
    data_processed = x + noise

pd.DataFrame(data_processed).to_csv(view.name_file, header=False)
