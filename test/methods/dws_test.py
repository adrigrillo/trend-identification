import matplotlib.pyplot as plt
import numpy as np

from src.methods.dws import DWS


class TestDiscreteWaveletSpectrum(object):
    def test_detect_no_trend(self):
        data_points = 1000
        x = np.arange(0, data_points)
        y = np.zeros((data_points,))
        season = np.sin(x + np.pi / 2)
        noise = np.random.normal(loc=0, scale=0.2, size=data_points)
        signal = y + season + noise

        dws = DWS()
        trend = dws.estimate_trend(x, signal)

        plt.plot(trend)
        plt.show()

        assert trend is None

    def test_detect_trend(self):
        data_points = 1000
        x = np.arange(0, data_points)
        y = x
        noise = np.random.normal(loc=0, scale=200, size=data_points)
        signal = y + noise

        plt.plot(signal)
        plt.show()

        dws = DWS()
        trend = dws.estimate_trend(x, signal)

        plt.plot(trend)
        plt.show()

        assert not trend

    def test_detect_base_case(self):
        data_points = 100
        x = np.arange(0, data_points)
        noise = np.random.normal(size=data_points)

        dws = DWS()
        trend = dws.estimate_trend(x, noise)

        assert trend is None

    def test_get_approximations(self):
        y = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        approximations = DWS()._get_approximations(y, 2, 'db1')

        first_level = [2.12132034, 4.94974747, 7.77817459, 10.60660172]
        second_level = [5., 13.]
        np.testing.assert_almost_equal(approximations[0], first_level)
        np.testing.assert_almost_equal(approximations[1], second_level)

    def test_calculate_signal_spectrum(self):
        signal_1 = [1, 1, 1, 1, 1, 1]
        signal_2 = [1, 3, 1, 3, 3, 1]
        spectrums = DWS()._calculate_signal_spectrum([signal_1, signal_2])

        np.testing.assert_approx_equal(spectrums[0], 0.0)
        np.testing.assert_approx_equal(spectrums[1], 1.0)
