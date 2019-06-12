import configparser
import glob
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.definitions import *
from src.methods.dws import DWS
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.method import Method
from src.methods.splines import Splines
from src.methods.theil import Theil
from src.utils import read_generated_csv, generate_timestamp, get_name_from_path


def trend_detection_comparison(methods_list: List[Method], file_prefix: str,
                               folder: str = GENERATED_DIR) -> pd.DataFrame:
    """
    Search for all the files in the folder, then perform the detection with the
    methods included in the list `methods_list` and generates a table with the
    return of every method.

    The table is saved in the `RESULTS_DIR` and also returned by the method.

    :param methods_list: list with the methods that will perform the detection
    :param file_prefix: prefix of the files that will be used
    :param folder: folder that will contain the files. Default: data/generated_data
    :return: table with the results of the different methods and results
    """
    files = list()
    results = dict()
    columns = [method.name for method in methods_list]
    timestamp = generate_timestamp()

    for file_path in glob.glob(f'{folder}/{file_prefix}*'):
        files.append(file_path)
    files.sort()  # sort by file name

    for file in files:
        file_results = list()
        name = get_name_from_path(file)

        x, y, trend, seasonality, noise = read_generated_csv(file)

        for method in methods_list:
            result = method.detect_trend(x, y)
            file_results.append(result)
        results[name] = file_results

    table = pd.DataFrame(results, columns)
    table.to_csv(f'{RESULTS_DIR}/trend_detection_{file_prefix}_{timestamp}.csv')

    return table


def trend_estimation_comparison(methods_list: List[Method], file_prefix: str,
                                folder: str = GENERATED_DIR, test_num: int = 5) -> pd.DataFrame:
    """
    Search for all the files in the folder, then perform the estimation with the
    methods included in the list `methods_list` and generates a table with the
    distance between the estimation and the ground truth.

    The method takes the mean between the number of executions to compare with the
    ground truth. It also generates the plots with the ground truth and the results
    of all the methods for the file.

    The table is saved in the `RESULTS_DIR` and also returned by the method.

    :param methods_list: list with the methods that will perform the detection
    :param file_prefix: prefix of the files that will be used
    :param folder: folder that will contain the files. Default: data/generated_data
    :param test_num: number of executions per method
    :return: table with the results of the different methods and results
    """
    files = list()
    results = dict()
    columns = [method.name for method in methods_list]
    timestamp = generate_timestamp()

    for file_path in glob.glob(f'{folder}/{file_prefix}*'):
        files.append(file_path)
    files.sort()  # sort by file name

    for file in files:
        file_results = list()
        name = get_name_from_path(file)

        params = configparser.ConfigParser(allow_no_value=True)
        params.read(f'{SYNTHETIC_DIR}/{name}.ini')

        x, y, trend, seasonality, noise = read_generated_csv(file)

        if params.has_option(TREND_DATA, FUNC):
            trend_title = params[TREND_DATA][FUNC]
        else:
            trend_title = 'Real data'
        if params.has_option(SEASONALITY_DATA, FUNC):
            seasonality_title = params[SEASONALITY_DATA][FUNC]
        else:
            seasonality_title = 'No seasonality'
        if params.has_option(NOISE_DATA, SIGNAL_TO_NOISE):
            noise_title = params[NOISE_DATA][SIGNAL_TO_NOISE]
        else:
            noise_title = 'No noise'

        # Set the plot
        plt.figure(figsize=(12, 8))
        plt.title(f'trend: {trend_title}, '
                  f'seasonality: {seasonality_title}, '
                  f'snr: {noise_title}')

        for method in methods_list:
            estimation = method.estimate_trend(x, y)
            plt.plot(x, estimation, label=method.name)

            distance = np.linalg.norm((estimation - trend))
            file_results.append(distance)

        plt.plot(x, trend, label='True trend', linewidth=3.0, color='k', linestyle=':')
        plt.legend()
        plt.savefig(f'{PLOTS_DIR}/{name}_{timestamp}.png')
        plt.close()

        results[name] = file_results

    table = pd.DataFrame(results, columns)
    table.to_csv(f'{RESULTS_DIR}/trend_estimation_{file_prefix}_{timestamp}.csv')

    return table


if __name__ == '__main__':
    # methods_detection = [MannKendall(), ITA(), Theil(), DWS(), EmpiricalModeDecomposition(),
    #                      HPfilter(), Splines()]
    #
    # trend_detection_comparison(methods_detection, 'func')

    methods_estimation = [Theil(), DWS(), EmpiricalModeDecomposition(), HPfilter(), Splines()]
    trend_estimation_comparison(methods_estimation, 'func')
