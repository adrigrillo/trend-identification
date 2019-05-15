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
        raise NotImplementedError('This method does not have the capability of detecting a trend')

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)

        # plt.figure(figsize=(6, 2))
        plt.plot(trend)
        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.title('Empirical Mode Decomposition')
        plt.show()
