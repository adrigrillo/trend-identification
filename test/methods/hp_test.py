from pandas.tests.extension.numpy_.test_numpy_nested import np

from src.methods.hp_filter import HPfilter


def test_estimate_trend():
    x = np.arange(0, 100)
    y = np.arange(0, 100)
    noise = np.random.normal(size=100)
    signal = y + noise

    estimation = HPfilter()
    cycle, trend = estimation.estimate_trend(x, signal)

    assert np.sum(y-trend)/y.shape[0] < 0.5
