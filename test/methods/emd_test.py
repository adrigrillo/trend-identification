import numpy as np

from src.methods.emd import EmpiricalModeDecomposition


def test_estimate_trend_linear():
    # test time series:
    x = np.arange(0, 3, 0.01)
    y = x

    emd = EmpiricalModeDecomposition()
    trend = emd.estimate_trend(x, y)
    np.testing.assert_almost_equal(y, trend)


def test_estimate_trend_non_linear():
    # test time series:
    x = np.arange(0, 3, 0.01)
    y = np.cos(22 / np.pi * x ** 2) + 6 * x ** 2

    emd = EmpiricalModeDecomposition()
    trend = emd.estimate_trend(x, y)
    np.testing.assert_approx_equal(0.52, trend[0], significant=1)
    np.testing.assert_approx_equal(53.36, trend[-1], significant=1)


def test_estimate_no_trend():
    # test time series:
    x = np.arange(0, 3, 0.01)
    y = np.empty(len(x))
    y.fill(0.5)

    emd = EmpiricalModeDecomposition()
    trend = emd.estimate_trend(x, y)
    np.testing.assert_almost_equal(y, trend)
