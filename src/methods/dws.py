from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler

from src.methods.method import Method


class DWS(Method):
    def __init__(self, wavelet: str = 'db8', confidence: float = 0.95, num_samples: int = 5000):
        """
        Instantiation method of the discrete wavelet spectrum.

        :param wavelet: name of the wavelet to be used
        """
        self.wavelet = wavelet
        self.confidence = confidence
        self.num_samples = num_samples
        self.scaler = MinMaxScaler(feature_range=(-1, 1))

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError

    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # 1. Normalize and decompose time series
        norm_time_series = self.scaler.fit_transform(time_series_y.reshape(-1, 1).astype(np.float64))

        # 2. Calculate DWS and spectrum value
        # TODO: this does not properly calculate the levels raise warning
        # max_level = int(np.floor(np.log2(len(time_series_y))))
        max_level = pywt.dwt_max_level(norm_time_series.shape[0], self.wavelet)

        signal_approximations = self._get_approximations(signal=norm_time_series,
                                                         levels=max_level,
                                                         wavelet=self.wavelet)
        signal_spectrum = self._calculate_signal_spectrum(signal_approximations)

        noise_spectrums = list()
        # 3. Generate noise & calculate RDWS
        for _ in range(self.num_samples):
            noise = np.random.normal(size=time_series_y.shape[0])
            noise = self.scaler.fit_transform(noise.reshape(-1, 1))

            noise_approximations = self._get_approximations(signal=noise,
                                                            levels=max_level,
                                                            wavelet=self.wavelet)
            noise_spectrum = self._calculate_signal_spectrum(noise_approximations)
            noise_spectrums.append(noise_spectrum)

        # 4. Calculate mean & variance of all RDWSs. Confidence interval = 95%
        noise_mean = np.mean(noise_spectrums, axis=0)
        noise_var = np.std(noise_spectrums, axis=0)
        confidence_intvl = stats.norm.interval(self.confidence, loc=noise_mean,
                                               scale=noise_var / np.sqrt(self.num_samples))
        # 5. Compare the spectrum of the n levels with the confidence level
        for level in range(max_level):
            if signal_spectrum[level] > confidence_intvl[1][level]:
                return signal_approximations[level]  # There is a trend
        return None

    @staticmethod
    def _get_approximations(signal, levels: int, wavelet: str):
        """
        Method that perform the discrete wavelet decomposition the number of
        levels indicated and saves all the approximation coefficient of the
        levels.

        :param signal: signal to decompose
        :param levels: number of levels for the discrete wavelet transform
        :param wavelet: name of the wavelet to be used
        :return: list with the approximation coefficient of each level
        """
        signal_approximations = list()
        for _ in range(levels):
            signal, _ = pywt.dwt(signal, wavelet)
            signal_approximations.append(signal)
        return signal_approximations

    @staticmethod
    def _calculate_signal_spectrum(signals: List):
        """
        Method that calculates the spectrum value of the signals given
        in a list.

        :param signals: signals to calculate the spectrum values
        :return: list with the spectrum values of each signal
        """
        spectrum_values = list()
        for signal in signals:
            spectrum_values.append(np.var(signal))
        return spectrum_values


if __name__ == '__main__':
    x = np.arange(100)
    noise = np.random.normal(loc=0, scale=5, size=100)
    y = np.cos(22 / np.pi * x) + 6 * x
    y = y + noise
    plt.plot(y)
    plt.show()
    dws = DWS()
    trend = dws.estimate_trend(x, x)
    plt.plot(trend)
    plt.show()
