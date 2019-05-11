import numpy as np

import pywt
import pywt.data
from sklearn.preprocessing import MinMaxScaler

from src.methods.method import Method


class DWS(Method):
    def __init__(self, save_name: str = 'dws_result',
                 save_path: str = '../../results/dws',
                 save_format: str = 'png'):
        """
        Instantiation method of the discrete wavelet spectrum.

        :param save_name: set the name of the file that contains the result
        :param save_path: set the path where the result will be saved
        :param save_format: set the file format of the result
        """
        self.save_path = save_path
        self.save_format = save_format
        self.save_name = save_name

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # 1. Normalize and decompose time series
        x_normalized = self.normalize(time_series_x)

        # 2. Calculate DWS

        # 3. Generate noise & calculate RDWS
        mu, sigma = 0, 1  # mean and standard deviation
        noise = np.random.normal(mu, sigma, len(time_series_y))
        noise = self.normalize(noise)

        # 4. Repeat 3. 5000 times, calculate mean & variance of all RDWSs. Confidence interval = 95%

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError

    def normalize(self, x: np.array):
        scaler = MinMaxScaler((-1, 1))
        return scaler.fit_transform(x)
