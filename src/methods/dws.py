from typing import List, Optional

import numpy as np
import pywt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

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
        self.series_scaler = MinMaxScaler(feature_range=(-1, 1))
        self.noise_scaler = MinMaxScaler(feature_range=(-1, 1))

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        return self.describe_trend_from_array(time_series_x, trend)

    def estimate_trend(self, time_series_x: np.ndarray,
                       time_series_y: np.ndarray) -> Optional[np.ndarray]:
        """
        Function used to execute the trend estimation process of the method

        :param time_series_x: time variable of the time series
        :param time_series_y: value of the time series
        :return: trend of the time series if no trend is detected. Otherwise, None
        """
        len_times_series = time_series_y.shape[0]

        # 1. Normalize and decompose time series
        norm_time_series = time_series_y.reshape(-1, 1).astype(np.float64)
        norm_time_series = self.series_scaler.fit_transform(norm_time_series)
        norm_time_series = norm_time_series.squeeze()

        max_level = pywt.dwt_max_level(len_times_series, self.wavelet)
        signal_approximations = self._get_approximations(norm_time_series, max_level)

        # 2. Calculate DWS and spectrum value
        signal_spectrum = self._calculate_signal_spectrum(signal_approximations)

        noise_spectra = list()
        # 3. Generate noise & calculate RDWS
        for _ in range(self.num_samples):
            noise = np.random.normal(size=(time_series_y.shape[0], 1))
            noise = self.noise_scaler.fit_transform(noise).squeeze()

            noise_approximations = self._get_approximations(noise, max_level)
            noise_spectrum = self._calculate_signal_spectrum(noise_approximations)

            noise_spectra.append(noise_spectrum)

        # 4. Calculate mean & variance of all RDWSs. Confidence interval = 95%
        noise_mean = np.mean(noise_spectra, axis=0)
        noise_var = np.std(noise_spectra, axis=0)
        confidence_intvl = stats.norm.interval(self.confidence, loc=noise_mean,
                                               scale=noise_var / np.sqrt(self.num_samples))
        # 5. Compare the spectrum of the n levels with the confidence level
        # check from the last decomposition (the trend) until the first
        for level in range(max_level - 1, -1, -1):
            if signal_spectrum[level] <= confidence_intvl[1][level]:
                return None
        trend = self._reconstruct_trend(signal_approximations[-1], max_level)
        return trend[:len_times_series]

    def _get_approximations(self, signal: np.ndarray, levels: int) -> List:
        """
        Method that perform the discrete wavelet decomposition the number of
        levels indicated and saves all the approximation coefficient of the
        levels.

        :param signal: signal to decompose
        :param levels: number of levels for the discrete wavelet transform
        :return: list with the approximation coefficient of each level
        """
        signal_approximations = list()
        for _ in range(levels):
            signal, _ = pywt.dwt(signal, self.wavelet)
            signal_approximations.append(signal)
        return signal_approximations

    def _reconstruct_trend(self, trend_approx: np.ndarray, levels: int) -> np.ndarray:
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

    @staticmethod
    def _calculate_signal_spectrum(signals: List) -> List:
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

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        super().visualize_trend(time_series_x, time_series_y, 'Discrete Wavelet Spectrum', 'Estimated trend')

# data_points = 300
# x = np.arange(0, data_points)
# y = 1 / 300 * x ** 2
# noise = np.random.normal(loc=0, scale=200, size=data_points)
# signal = y + noise
#
# plt.plot(x, signal)
# plt.show()
#
# dws = DWS()
# trend = dws.estimate_trend(x, signal)
# plt.plot(x, trend)
# plt.show()
