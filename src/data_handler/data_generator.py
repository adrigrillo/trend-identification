import random

import numpy as np
from src.data_handler.data_handler import generate_synthetic_data
from src.data_handler.data_handler import create_function_file

# Generate time series with trend, seasonality and noise

name = 'time_series_'
fun_max_degree = 3
fun_slope_steps = 5
data_points = 300
#mean = 0
#deviations = [0.1, 0.5, 1]
sig_noise_ratio = [0, 0.25, 0.5, 0.75]
seasonalities = ['np.sin(y)', 'np.sin(3*y)+2*np.cos(y)']


# generate trend functions:
polynomials = [''] * (fun_max_degree * fun_slope_steps)
#sinusoidals = [''] * (fun_max_degree * fun_slope_steps)
sinusoidals = ['np.sin(310*x)', 'np.sin(410*x)',
               '10*np.sin(310*x)', '10*np.sin(410*x)',
               '100*np.sin(310*x)', '100*np.sin(410*x)']

# TODO: generate sinusoidals correctly
for i in range(len(polynomials)):
    for degree in range(1, fun_max_degree+1):
        for slope in range(1, fun_slope_steps+1):
            if slope:
                polynomials[i] = str(round(random.uniform(-1, 1), 2)) + '*x**' + str(degree)
                #sinusoidals[i] = str(round(random.uniform(-10, 10), 2)) + \
                #                 '*np.sin(' + \
                #                 str(round(random.uniform(0.6, 1), 2)*2*np.pi/300) + \
                #                 '*x)'

trends = polynomials + sinusoidals

number_generated_time_series = len(trends) * len(sig_noise_ratio) * len(seasonalities)
generated_xs = \
    generated_ys = \
    generated_trends = \
    generated_seasonalities = \
    generated_noises = \
    [[0] for y in range(number_generated_time_series)]

index = 0
for trend in trends:
    for noise in sig_noise_ratio:
        for seasonality in seasonalities:
            index += 1
            # create .ini function file
            create_function_file(name + str(index), trend, data_points, noise, seasonality)
            # create .cvs data file
            generated_xs[index-1], \
                generated_ys[index-1], \
                generated_trends[index-1], \
                generated_seasonalities[index-1], \
                generated_noises[index-1] = \
                generate_synthetic_data('function', name + str(index) + '.ini')
