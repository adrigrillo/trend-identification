from PyEMD import EMD, Visualisation
from src.methods.method import Method
import matplotlib.pyplot as plt
import numpy as np


class EmpiricalModeDecomposition(Method):
    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Extract imfs and residue
        emd = EMD()
        emd.emd(time_series_x)
        imfs, res = emd.get_imfs_and_residue()
        return imfs[-1]

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        raise NotImplementedError('This method does not have the capability of detecting a trend')

    def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)

        plt.figure(figsize=(6, 2))
        plt.plot(trend)
        plt.xlabel('Time')
        plt.ylabel('Trend')
        plt.show()


# test time series:
t = np.arange(0, 3, 0.01)
S = np.sin(13*t + 0.2*t**1.4) - np.cos(3*t)
S1 = t
S2 = np.cos(22 / np.pi * t**2) + 6 * t**2
S3 = np.empty(len(t))
S3.fill(0.5)

emd = EmpiricalModeDecomposition()
emd.visualize_trend(S1, t)





