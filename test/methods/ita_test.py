import os
import uuid

import numpy as np

from src.methods.ita import ITA


def test_detect_trend():
    x = np.arange(0, 100)
    y = np.arange(0, 100)
    noise = np.random.normal(size=100)
    signal = y + noise

    file_id = str(uuid.uuid1())

    ita = ITA()
    ita.detect_trend(time_series_x=x, time_series_y=signal, file_id=file_id, plot=True)

    file_found = False
    results_folder = '../../results/ita/'
    for root, dirs, files in os.walk(results_folder):
        for file in files:
            if file_id in file:
                file_found = True
                os.remove(results_folder + file)
    assert file_found
