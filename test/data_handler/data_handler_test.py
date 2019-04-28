# -*- coding: utf-8 -*-
"""
data_handler_test.py
=================
Tests for the data_handler.py methods.
"""
import sys

from src.data_handler.data_handler import generate_synthetic_data
from src.definitions import ROOT_DIR


def test_generate_synthetic_data_from_data():
    generate_synthetic_data(method='data', config_file_name='from_data.ini')
