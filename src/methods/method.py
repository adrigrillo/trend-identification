# -*- coding: utf-8 -*-
"""
method.py
=================
Abstract class that all the methods will import in order to have a generalized
structure. Every method will implement their specific functionality.
"""
import abc
import numpy as np


class Method(abc.ABC):
    @abc.abstractmethod
    def detect_trend(self, time_series: np.ndarray):
        raise NotImplementedError
