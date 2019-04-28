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
from scipy.io import loadmat

from src.definitions import SYNTHETIC_DIR, FILE_DATA, DATA_DIR, FILE_NAME, MATLAB, CSV, X_COL, Y_COL, HEADER


def load_data():
    pass


def generate_synthetic_data(method: str, config_file_name: str):
    if method is 'func':
        # generate data using a function
        pass
    elif method is 'data':
        # generate data using data
        config = configparser.ConfigParser(allow_no_value=True)
        config_file_path = SYNTHETIC_DIR + '/' + config_file_name
        config.read(config_file_path)
        generate_from_data(config)
    else:
        raise AttributeError('The method {0} does not match with any valid option (func or data)'.format(method))


def generate_from_data(generation_params: configparser.ConfigParser):
    sections = generation_params.sections()
    if FILE_DATA in sections:
        file_loader(generation_params[FILE_DATA])

    print(generation_params.sections())


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
            header: bool = file_params.getboolean(HEADER)
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

    values_x = data_squeezer(data_file[x_col])
    values_y = data_squeezer(data_file[y_col])

    return values_x, values_y


def data_squeezer(data: np.ndarray) -> np.ndarray:
    """
    Method to transform a numpy array to a one dimension array

    :param data: data in numpy array
    :return: one dimensional numpy array
    """
    while len(data.shape) != 1:
        data = data.squeeze()
    return data
