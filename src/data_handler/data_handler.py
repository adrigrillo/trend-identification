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

from src.definitions import SYNTHETIC_DIR


def load_data():
    pass


def generate_synthetic_data(method: str, config_file_name: str):
    if method is 'func':
        # generate data using a function
        pass
    elif method is 'data':
        # generate data using data
        config = configparser.ConfigParser(allow_no_value=True)
        config_file_path = SYNTHETIC_DIR + config_file_name
        config.read(config_file_path)
        generate_from_data(config)
    else:
        raise AttributeError('The method {0} does not match with any valid option (func or data)'.format(method))


def generate_from_data(data_file: configparser.ConfigParser):
    print(data_file.sections())
