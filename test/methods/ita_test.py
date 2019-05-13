import os
import uuid

import numpy as np

from src.methods.ita import ITA


class TestInnovativeTrendAnalysis(object):
    def test_detect_no_trend(self):
        x = np.arange(0, 100)
        y = np.zeros((100,))
        season = np.sin(x + np.pi / 2)
        noise = np.random.normal(loc=0, scale=0.2, size=100)
        signal = y + season + noise

        file_id = str(
            uuid.uuid1())  # 1 structuring data handler. Starting with the implementation with the low-pass method

        ita = ITA(file_id=file_id)
        trend = ita.detect_trend(x, signal)
        assert not trend

        file_found = False
        results_folder = '../../results/ita/'
        for root, dirs, files in os.walk(results_folder):
            for file in files:
                if file_id in file:
                    file_found = True
                    os.remove(results_folder + file)
        assert file_found

    def test_detect_trend(self):
        x = np.arange(0, 100)
        y = x
        noise = np.random.normal(loc=0, scale=5, size=100)
        signal = y + noise

        file_id = str(
            uuid.uuid1())  # 1 structuring data handler. Starting with the implementation with the low-pass method

        ita = ITA(file_id=file_id)

        trend = ita.detect_trend(x, signal)
        assert trend

        file_found = False
        results_folder = '../../results/ita/'
        for root, dirs, files in os.walk(results_folder):
            for file in files:
                if file_id in file:
                    file_found = True
                    os.remove(results_folder + file)
        assert file_found
