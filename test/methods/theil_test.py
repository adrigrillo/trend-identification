import numpy as np

from src.methods.theil import Theil


def test_base_case():
    x = np.arange(0, 100)
    y = np.arange(0, 100)
    noise = np.random.normal(scale=10, size=100)
    signal = y + noise

    theil = Theil()
    trend = theil.estimate_trend(x, signal)

    assert signal.shape[0] == trend.shape[0]
