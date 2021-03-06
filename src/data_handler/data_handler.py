# -*- coding: utf-8 -*-
"""
data_handler.py
=================
Main class used for the synthetic and loading of the datasets. This class implements two
functions:

- **Generation of synthetic data**: this could be done indicating a function that will
  be the trend or using a real dataset that will be low-pass filtered to generate a trend.
  In both cases, the generated trend will be hidden adding noise and seasonality.

- **Loading of real datasets to be used in the system**: this will load the data and adapt
  it to be used by the system.
"""
import configparser
from os.path import splitext
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import pywt
from pywt import downcoef
from scipy.io import loadmat

from src.definitions import *


def generate_synthetic_data(method: str, config_file_name: str) -> Tuple:
    """
    Generate a time series from specified data in the .ini files. Check the
    example .ini files to understand the structure.

    This method allows two ways of creating synthetic data from a function,
    that will be the trend, or from a previous time series, that is smoothed with
    discrete wavelet transform. Then seasonality components and noise can be added
    to the trend.

    :param method: 'function' if the trend data comes from a function or 'data'
    if it comes from a existing dataset.
    :param config_file_name: name of the .ini file. Ex: 'test_func.ini'
    :return: data for the generated time series, normalised. It returns
    the x-axis data, the y-axis data, the trend data, the seasonality and the noise
    """
    config_file_path = SYNTHETIC_DIR + '/' + config_file_name

    generation_params = configparser.ConfigParser(allow_no_value=True)
    generation_params.read(config_file_path)

    sections = generation_params.sections()

    if FILE_DATA in sections or TREND_DATA in sections:
        if method is 'function':
            # generate data using a function
            x_values, trend_values = generate_trend(generation_params[TREND_DATA])
        elif method is 'data':
            # generate data using data
            file_params = generation_params[FILE_DATA]
            x_values, trend_values = file_loader(file_params)
            # trend_values = smooth_for_trend(trend_values, file_params)
            # Set x between 0 and 1 after getting the trend with desired length
            x_values = np.linspace(0, 1, trend_values.shape[0])
        else:
            raise AttributeError('The method {0} does not match with any valid option (func or data).'.format(method))
        data_points = trend_values.shape[0]
        if x_values.shape[0] > data_points:
            x_values = np.take(x_values, np.arange(data_points))
    else:
        raise ValueError('The configuration file does not contain any data to generate the trend.')

    seasonality_values = np.zeros(data_points)
    if SEASONALITY_DATA in sections:
        seasonality_values = generate_seasonality(generation_params[SEASONALITY_DATA], data_points)

    noise_values = np.zeros(data_points)
    if NOISE_DATA in sections:
        noise_values = generate_noise(generation_params[NOISE_DATA],
                                      trend_values + seasonality_values, data_points)

    y_values: np.ndarray = trend_values + seasonality_values + noise_values
    time_series = np.array([x_values, y_values, trend_values, seasonality_values, noise_values]).T

    output_path = GENERATED_DIR + '/' + generation_params[SAVE_DATA][FILE_NAME]
    header = ['x', 'y', 'trend', 'seasonality', 'noise']
    pd.DataFrame(time_series).to_csv(output_path, header=header)

    return x_values, y_values, trend_values, seasonality_values, noise_values


def file_loader(file_params: configparser.ConfigParser) -> Tuple[np.ndarray, np.ndarray]:
    """
    Method that uses the configuration relative to the data file ([file]) to
    read the file ('.mat' or '.csv') containing the data of the time series and
    returns the values of the axis x and axis y of it, in two different numpy arrays.

    The configuration has to be contain the following parameter:

    - **filename**: Name of the file, contained in the data directory
    - **header**: for CSV only, boolean indicating if the file contains a header
    - **x_column**: int (no header) or string (header or .mat) where the x values are
    - **y_column**: int (no header) or string (header or .mat) where the y values are

    Example 1:

    ```\n
    [file]\n
    filename=test.csv\n
    header=False\n
    x_column=0\n
    y_column=1\n
    ```

    Example 2:

    ```\n
    [file]\n
    filename=test_header.csv\n
    header=True\n
    x_column=date\n
    y_column=high\n
    ```

    :param file_params: parameters relative to the file to load
    :return: values of x and values of y
    """
    x_col = file_params[X_COL]
    y_col = file_params[Y_COL]
    file_name = file_params[FILE_NAME]
    file_path = DATA_DIR + '/' + file_name

    if Path(file_path).is_file():
        extension = splitext(file_name)[1]
        if extension == MATLAB:
            data_file = loadmat(file_path)
        elif extension == CSV:
            header: bool = file_params.getboolean(HEADER, fallback=False)
            if header:
                header_flag = 'infer'
            else:
                header_flag = None
                # Transform to take the column number
                x_col = int(x_col)
                y_col = int(y_col)
            data_file = pd.read_csv(file_path, header=header_flag)
        else:
            raise ImportError('The file format is not supported, only {0} and {1} are supported'.format(MATLAB, CSV))
    else:
        raise FileNotFoundError

    y_values = data_squeezer(data_file[y_col])

    if x_col != 'None':
        x_values = data_squeezer(data_file[x_col])
    else:
        x_values = np.arange(y_values.shape[0])

    return x_values, y_values


def generate_trend(trend_params: configparser.ConfigParser) -> Tuple[np.ndarray, np.ndarray]:
    """
    Method that generates the underlying trend of the time series using the function specified in the trend
    section of the configuration ([trend]).

    The trend function must be defined in the configuration file as python code and is evaluated
    using the `eval()` function in python. As the result has to be a numpy array, the set of
    function admitted should use the **numpy library** referring at it like np.

    It needs also the number of data point that will be contained in the time series. An example is:

    ```\n
    [trend]\n
    function=(1/5*x)**2-x\n
    data_points=300
    ```

    :param trend_params: parameters relative to the trend
    :return: data points that represent the time series seasonality component
    """
    function = trend_params[FUNC]
    data_points = int(trend_params[DATA_PTS])
    x = np.linspace(0, 1, data_points)
    y = eval(function)
    return x, np.array(y)


def generate_seasonality(seasonality_params: configparser.ConfigParser, data_points: int) -> np.ndarray:
    """
    Method that uses the configuration relative to the seasonality ([seasonality]) and the
    number of data points required to generate a numpy array with the values that represent
    the seasonality of the system.

    The seasonality must be defined in the configuration file as python code and is evaluated
    using the `eval()` function in python. As the result has to be a numpy array, the set of
    function admitted should use the **numpy library** referring at it like np. An example is:

    ```\n
    [seasonality]\n
    function=np.sin(y)+np.cos(y/2)\n
    ```

    :param seasonality_params: parameters relative to the seasonality
    :param data_points: number of data points of the series
    :return: data points that represent the time series seasonality component
    """
    y: np.ndarray = np.arange(data_points)  # this will be used by the function
    func: str = seasonality_params[FUNC]
    return np.array(eval(func))


def generate_noise(noise_params: configparser.ConfigParser, signal: np.ndarray,
                   data_points: int) -> np.ndarray:
    """
    Method that uses the configuration relative to the noise ([noise]) and the number of
    data points required to generate a numpy array with the values that represent the noise
    of the system.

    :param noise_params: parameters relative to the noise
    :param signal: the signal to what we will add noise
    :param data_points: number of data points of the series
    :return: data points that represent the white gaussian noise
    """
    snr = float(noise_params[SIGNAL_TO_NOISE])
    if snr != 0.0:
        noise = np.random.normal(size=data_points)
        # work out the current SNR
        current_snr = np.mean(signal) / np.std(noise)
        # scale the noise by the snr ratios (smaller noise <=> larger snr)
        noise *= (current_snr / snr)
    else:
        noise = np.zeros(data_points)
    # return the new signal with noise
    return noise


def smooth_for_trend(y_values: np.ndarray, smooth_params: configparser.ConfigParser) -> np.ndarray:
    """
    Method that smooth a time series using wavelet transforms. In the configuration file ([file])
    the type of wavelet, the number of transforms and the desired length of the results is given
    in order to perform the operation.

    Remember that if the length of the result is smaller than the desired length, the
    computation of the transformations will be halted. Moreover, if the first iteration
    already gives a shorter time series an exception will be raised.

    An example of configuration is:
    ```\n
    [file]\n
    ...\n
    wavelet=db8 #wavelet type\n
    levels=5 #transformation levels\n
    data_points=300 #desired length\n
    ```

    :param y_values: y values of the original time series
    :param smooth_params: parameters relative to the smoothing
    :return: smoothed time series that will be used as trend
    """
    wavelet = smooth_params[WAVELET]
    levels = pywt.dwt_max_level(y_values.shape[0], wavelet)
    data_points = int(smooth_params[DATA_PTS])

    # Decompose getting only the details
    for _ in range(levels):
        y_values = downcoef(part='a', data=y_values, wavelet=wavelet)

    for _ in range(levels):
        details = np.zeros(y_values.shape)
        y_values = pywt.idwt(y_values, details, wavelet=wavelet)

    if y_values.shape[0] > data_points:
        return y_values[:data_points]
    else:
        raise ValueError('The original time series is to short to perform this operation')


def reconstruct_trend(self, trend_approx: np.ndarray, levels: int) -> np.ndarray:
    """
    Method that reconstructs the time series trend from its approximation.

    All the details coefficients are set to 0 to only reconstruct the
    trend.

    :param trend_approx: approximation of the trend
    :param levels: number of decomposition made in the original time series
    :return: reconstructed trend of the time series
    """
    for _ in range(levels):
        details = np.zeros(trend_approx.shape)
        trend_approx = pywt.idwt(trend_approx, details, self.wavelet)
    trend = self.series_scaler.inverse_transform(trend_approx.reshape(-1, 1))
    return trend.squeeze()


def data_squeezer(data: np.ndarray) -> np.ndarray:
    """
    Method to transform a numpy array to a one dimension array

    :param data: data in numpy array
    :return: one dimensional numpy array
    """
    if isinstance(data, pd.Series):
        data = data.to_numpy()
    while len(data.shape) != 1:
        data = data.squeeze()
    return data


def create_function_file_synthetic(name: str, trend: str, data_points: int, signal_to_noise: float, seasonality: str, coefs: [float], function_form: str):
    config = configparser.ConfigParser()
    config['trend'] = {'function': trend, 'function_form':function_form, 'data_points': str(data_points), 'a':coefs[0], 'b': coefs[1], 'c':coefs[2]}
    config['noise'] = {'signal_to_noise': str(signal_to_noise)}
    config['seasonality'] = {'function': seasonality}
    config['save'] = {'filename': name + '.csv'}
    with open(SYNTHETIC_DIR + '/' + name + '.ini', 'w') as configfile:
        config.write(configfile)


def create_function_file_pseudoreal(index: int, name: str, header: bool, x_col: str, y_col: str, wavelet: str, data_points: int, signal_to_noise: float, seasonality: str):
    config = configparser.ConfigParser()
    config['trend'] = {'function_form': name}
    config['file'] = {'filename': name + '.csv', 'header': header, 'x_column': x_col, 'y_column': y_col, 'wavelet': wavelet, 'data_points': data_points}
    config['noise'] = {'signal_to_noise': str(signal_to_noise)}
    config['seasonality'] = {'function': seasonality}
    config['save'] = {'filename': name + str(index) + '.csv'}
    with open(SYNTHETIC_DIR + '/' + name + str(index) + '.ini', 'w') as configfile:
        config.write(configfile)

