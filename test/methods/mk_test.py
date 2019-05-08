import numpy as np

from src.methods.mk import MannKendall


class TestMannKendall():
    def test_detect_no_trend(self):
        x = np.zeros((100,))
        y = np.zeros((100,))
        noise = np.random.normal(size=100)
        signal = y + noise

        mk = MannKendall()
        trend, trend_type, p, z = mk.detect_trend(x, signal)

        assert not trend
        assert trend_type == 'no trend'

    def test_detect_decreasing_trend(self):
        x = np.linspace(100, 0, num=100)
        y = np.linspace(100, 0, num=100)
        noise = np.random.normal(size=100)
        signal = y + noise

        mk = MannKendall()
        trend, trend_type, p, z = mk.detect_trend(x, signal)

        assert trend
        assert trend_type == 'decreasing'

    def test_detect_increasing_trend(self):
        x = np.arange(0, 100)
        y = np.arange(0, 100)
        noise = np.random.normal(size=100)
        signal = y + noise

        mk = MannKendall()
        trend, trend_type, p, z = mk.detect_trend(x, signal)

        assert trend
        assert trend_type == 'increasing'
