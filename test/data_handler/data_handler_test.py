# -*- coding: utf-8 -*-
"""
data_handler_test.py
=================
Tests for the data_handler.py methods.
"""
import configparser

import numpy as np
import pytest

from src.data_handler.data_handler import file_loader, generate_noise, generate_seasonality
from src.definitions import SYNTHETIC_DIR, FILE_DATA, NOISE_DATA, MEAN, DEVIATION, SEASONALITY_DATA


class TestFileLoader(object):
    def test_file_loader_mat(self):
        configuration = obtain_config(config_file_name='test_mat.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert len(x) == 10000 and len(y) == 10000

    def test_file_loader_csv(self):
        configuration = obtain_config(config_file_name='test_csv.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert len(x) == 100 and len(y) == 100
        assert x[0] == 0

    def test_file_loader_csv_header(self):
        configuration = obtain_config(config_file_name='test_csv_header.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert len(x) == 4999 and len(y) == 4999


class TestNoiseGenerator(object):
    def test_noise_generation(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv.ini')

        noise = generate_noise(configuration[NOISE_DATA], data_points=data_points)

        np.random.seed(797)
        mean = int(configuration[NOISE_DATA][MEAN])
        deviation = int(configuration[NOISE_DATA][DEVIATION])
        test_noise = np.random.normal(mean, deviation, data_points)

        assert len(noise) == data_points
        np.testing.assert_almost_equal(noise, test_noise)

    def test_noise_generation_fail(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv.ini')

        noise = generate_noise(configuration[NOISE_DATA], data_points=data_points)

        mean = int(configuration[NOISE_DATA][MEAN])
        deviation = int(configuration[NOISE_DATA][DEVIATION])
        test_noise = np.random.normal(mean, deviation, data_points)

        assert len(noise) == data_points
        np.testing.assert_raises(AssertionError, np.testing.assert_array_equal, noise, test_noise)


class TestSeasonalityGenerator(object):
    def test_seasonality_generation(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv.ini')

        seasonality = generate_seasonality(configuration[SEASONALITY_DATA], data_points=data_points)

        y = np.arange(data_points)
        values = np.sin(y)

        assert len(seasonality) == data_points
        np.testing.assert_equal(seasonality, values)

    def test_noise_generation_complex(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv_header.ini')

        seasonality = generate_seasonality(configuration[SEASONALITY_DATA], data_points=data_points)

        y = np.arange(data_points)
        values = np.sin(y) + np.cos(y / 2)

        assert len(seasonality) == data_points
        np.testing.assert_equal(seasonality, values)

    def test_noise_generation_error_bad_func_def(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_mat.ini')

        with pytest.raises(NameError):
            generate_seasonality(configuration[SEASONALITY_DATA], data_points=data_points)


def obtain_config(config_file_name: str) -> configparser.ConfigParser:
    """
    Read the config file

    :param config_file_name: name of the file
    :return: parameters in the config file
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config_file_path = SYNTHETIC_DIR + '/' + config_file_name
    config.read(config_file_path)
    return config
