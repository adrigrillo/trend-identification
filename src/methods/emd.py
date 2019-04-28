from PyEMD import EMD, Visualisation
from src.methods.method import Method
import numpy as np


class EmpiricalModeDecomposition(Method):
    def estimate_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        # Extract imfs and residue
        emd = EMD()
        emd.emd(time_series_x)
        imfs, res = emd.get_imfs_and_residue()
        return imfs[:-1]

    def detect_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):
        trend = self.estimate_trend(time_series_x, time_series_y)
        threshold = 0.05
        if np.abs(trend[:-1] - trend[0]) > threshold:
            return True
        else:
            return False



    #def visualize_trend(self, time_series_x: np.ndarray, time_series_y: np.ndarray):


t = np.arange(0, 3, 0.01)
S = np.sin(13*t + 0.2*t**1.4) - np.cos(3*t)
S1 = t
S2 = np.cos(22 / np.pi * t**2) + 6 * t**2
S3 = np.empty(len(t))
S3.fill(0.5)

emd_test = EMD()
emd_test.emd(S)
imfs_test, res_test = emd_test.get_imfs_and_residue()

print(imfs_test[0])
print(imfs_test[1])

vis = Visualisation()
vis.plot_imfs(imfs=imfs_test, residue=res_test, t=t, include_residue=True)
vis.show()
