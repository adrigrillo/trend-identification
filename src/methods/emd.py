import matplotlib.pyplot as plt
import numpy as np
from PyEMD import EMD

from src.methods.method import Method


class EmpiricalModeDecomposition(Method):
    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Extract imfs and residue
        emd = EMD()
        emd.emd(time_series_y)
        imfs, res = emd.get_imfs_and_residue()
        return imfs[-1]

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        return self.describe_trend_from_array(time_series_x, trend)

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)

        plt.plot(trend)
        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.title('Empirical Mode Decomposition')
        plt.show()
