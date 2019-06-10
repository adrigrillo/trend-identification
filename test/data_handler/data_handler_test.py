# -*- coding: utf-8 -*-
"""
data_handler_test.py
=================
Tests for the data_handler.py methods.
"""
import os

import pytest

from src.data_handler.data_handler import *
from src.definitions import *


class TestGenerateSyntheticData(object):
    def test_generation_by_function(self):
        file_name = 'test_func.ini'
        x, y, trend, seasonality, noise = generate_synthetic_data('function', file_name)

        configuration = obtain_config(config_file_name=file_name)
        output_name = configuration[SAVE_DATA][FILE_NAME]
        output_path = GENERATED_DIR + '/' + output_name

        if Path(output_path).is_file():
            data = pd.read_csv(output_path)
            read_x = np.array(data['x'])
            read_y = np.array(data['y'])
            read_trend = np.array(data['trend'])
            read_seasonality = np.array(data['seasonality'])
            read_noise = np.array(data['noise'])
            np.testing.assert_almost_equal(x, read_x)
            np.testing.assert_almost_equal(y, read_y)  # almost because of precision float
            np.testing.assert_almost_equal(trend, read_trend)  # almost because of precision float
            np.testing.assert_almost_equal(seasonality, read_seasonality)  # almost because of precision float
            np.testing.assert_almost_equal(noise, read_noise)  # almost because of precision float
            os.remove(output_path)
        else:
            pytest.fail('The file was not written')

    def test_generation_by_data_csv(self):
        file_name = 'test_csv_header.ini'
        x, y, trend, seasonality, noise = generate_synthetic_data('data', file_name)

        configuration = obtain_config(config_file_name=file_name)
        output_name = configuration[SAVE_DATA][FILE_NAME]
        output_path = GENERATED_DIR + '/' + output_name

        if Path(output_path).is_file():
            data = pd.read_csv(output_path)
            read_x = np.array(data['x']).T
            read_y = np.array(data['y']).T
            read_trend = np.array(data['trend']).T
            read_seasonality = np.array(data['seasonality']).T
            read_noise = np.array(data['noise']).T
            np.testing.assert_equal(x, read_x)
            np.testing.assert_almost_equal(y, read_y)  # almost because of precision float
            np.testing.assert_almost_equal(trend, read_trend)  # almost because of precision float
            np.testing.assert_almost_equal(seasonality, read_seasonality)  # almost because of precision float
            np.testing.assert_almost_equal(noise, read_noise)  # almost because of precision float
            os.remove(output_path)
        else:
            pytest.fail('The file was not written')

    def test_generation_by_data_mat(self):
        file_name = 'test_mat.ini'
        x, y, trend, seasonality, noise = generate_synthetic_data('data', file_name)

        configuration = obtain_config(config_file_name=file_name)
        output_name = configuration[SAVE_DATA][FILE_NAME]
        output_path = GENERATED_DIR + '/' + output_name

        if Path(output_path).is_file():
            data = pd.read_csv(output_path)
            read_x = np.array(data['x']).T
            read_y = np.array(data['y']).T
            read_trend = np.array(data['trend']).T
            read_seasonality = np.array(data['seasonality']).T
            read_noise = np.array(data['noise']).T
            np.testing.assert_equal(x, read_x)
            np.testing.assert_almost_equal(y, read_y)  # almost because of precision float
            np.testing.assert_almost_equal(trend, read_trend)  # almost because of precision float
            np.testing.assert_almost_equal(seasonality, read_seasonality)  # almost because of precision float
            np.testing.assert_almost_equal(noise, read_noise)  # almost because of precision float
            os.remove(output_path)
        else:
            pytest.fail('The file was not written')

    def test_generation_by_file_error_short(self):
        file_name = 'test_csv.ini'

        with pytest.raises(ValueError):
            generate_synthetic_data('data', file_name)

    def test_file_loader_mat(self):
        configuration = obtain_config(config_file_name='test_mat.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert x.shape[0] == 1000
        assert y.shape[0] == 1000

    def test_file_loader_csv(self):
        configuration = obtain_config(config_file_name='test_csv.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert x.shape[0] == 100
        assert y.shape[0] == 100
        assert x[0] == 0

    def test_file_loader_csv_header(self):
        configuration = obtain_config(config_file_name='test_csv_header.ini')
        x, y = file_loader(configuration[FILE_DATA])
        assert x.shape[0] == 4999
        assert y.shape[0] == 4999

    def test_trend_generation(self):
        configuration = obtain_config(config_file_name='test_func.ini')
        x, y = generate_trend(configuration[TREND_DATA])

        data_points = int(configuration[TREND_DATA][DATA_PTS])
        x_test = np.linspace(0, 1, data_points)
        y_test = np.array((1 / 5 * x_test) ** 2 - x_test)

        assert x.shape[0] == data_points
        np.testing.assert_equal(y, y_test)

    def test_function_smoothing(self):
        file_name = 'test_mat.ini'
        configuration = obtain_config(config_file_name=file_name)[FILE_DATA]

        path = DATA_DIR + '/' + configuration[FILE_NAME]
        signal = data_squeezer(loadmat(path)[configuration[Y_COL]])

        y_values = smooth_for_trend(signal, configuration)

        assert y_values.shape[0] == int(configuration[DATA_PTS])

    def test_noise_generation(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv.ini')

        np.random.seed(797)
        noise = generate_noise(configuration[NOISE_DATA], np.arange(data_points), data_points)

        np.testing.assert_almost_equal(noise, np.zeros(data_points))

    def test_noise_generation_fail(self):
        data_points = 5
        configuration = obtain_config(config_file_name='test_csv_header.ini')

        np.random.seed(797)
        noise = generate_noise(configuration[NOISE_DATA], np.arange(data_points), data_points)

        test_noise = np.array([2.70578832, -4.07251312, 8.32160285, 3.91816287, 3.8628272])
        assert len(noise) == data_points
        np.testing.assert_raises(AssertionError, np.testing.assert_array_equal, noise, test_noise)

    def test_seasonality_generation(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv.ini')

        seasonality = generate_seasonality(configuration[SEASONALITY_DATA], data_points=data_points)

        y = np.arange(data_points)
        values = np.sin(y)

        assert len(seasonality) == data_points
        np.testing.assert_equal(seasonality, values)

    def test_seasonality_generation_complex(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_csv_header.ini')

        seasonality = generate_seasonality(configuration[SEASONALITY_DATA], data_points=data_points)

        y = np.arange(data_points)
        values = np.sin(y) + np.cos(y / 2)

        assert len(seasonality) == data_points
        np.testing.assert_equal(seasonality, values)

    def test_seasonality_generation_error_bad_func_def(self):
        data_points = 100
        configuration = obtain_config(config_file_name='test_mat.ini')

        with pytest.raises(NameError):
            configuration.set(SEASONALITY_DATA, FUNC, 'np.sin(x)')
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
