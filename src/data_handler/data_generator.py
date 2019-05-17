import numpy as np
from src.data_handler.data_handler import generate_synthetic_data
from src.data_handler.data_handler import create_function_file

# Generate time series with trend, seasonality and noise

name = 'time_series_'
fun_max_degree = 5
fun_slope_steps = 3
data_points = 300
mean = 0
deviations = [1, 5, 10]
seasonalities = ['np.sin(y)', 'np.sin(3*y)+2*np.cos(y)']


# generate trend functions:
polynomials = [''] * (fun_max_degree * fun_slope_steps * 2)
sinusoidals = [''] * (fun_max_degree * fun_slope_steps * 2)

# TODO: generate sinusoidals correctly
for i in range(len(polynomials)):
    for degree in range(1, fun_max_degree+1):
        for slope in range(-fun_slope_steps, fun_slope_steps+1):
            if slope != 0:
                polynomials[i] = str(round(1/slope, 2)) + '*x**' + str(degree)
                sinusoidals[i] = str(round(1/slope, 2)) + '*np.sin(' + str(degree) + '*x)'

trends = polynomials + sinusoidals

number_generated_time_series = len(trends) * len(deviations) * len(seasonalities)
generated_xs = \
    generated_ys = \
    generated_trends = \
    generated_seasonalities = \
    generated_noises = \
    [[0] for y in range(number_generated_time_series)]
    #np.zeros(number_generated_time_series)

index = 0
for trend in trends:
    for deviation in deviations:
        for seasonality in seasonalities:
            index += 1
            # create .ini function file
            create_function_file(name + str(index), trend, data_points, mean, deviation, seasonality)
            # create .cvs data file
            generated_xs[index-1], \
                generated_ys[index-1], \
                generated_trends[index-1], \
                generated_seasonalities[index-1], \
                generated_noises[index-1] = \
                generate_synthetic_data('function', name + str(index) + '.ini')
