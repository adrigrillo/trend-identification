import os
import uuid

import numpy as np
import matplotlib.pyplot as plt

from src.methods.ita import ITA


def test_detect_no_trend():
    x = np.arange(0, 100)
    y = 100 * np.sin(x / 7)
    noise = np.random.normal(loc=0, scale=25, size=100)
    signal = y + noise

    file_id = str(uuid.uuid1())  # 1 structuring data handler. Starting with the implementation with the low-pass method

    ita = ITA(file_id=file_id, plot=True)
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


def test_detect_trend():
    x = np.arange(0, 100)
    y = x
    noise = np.random.normal(loc=0, scale=25, size=100)
    signal = y + noise

    plt.plot(signal)
    plt.show()

    file_id = str(uuid.uuid1())  # 1 structuring data handler. Starting with the implementation with the low-pass method

    ita = ITA(file_id=file_id, plot=True)

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
