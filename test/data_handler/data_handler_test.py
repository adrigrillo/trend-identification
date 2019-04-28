# -*- coding: utf-8 -*-
"""
data_handler_test.py
=================
Tests for the data_handler.py methods.
"""
import configparser

from src.data_handler.data_handler import file_loader
from src.definitions import SYNTHETIC_DIR, FILE_DATA


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
