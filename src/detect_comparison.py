import glob
from datetime import datetime
from typing import List

import pandas as pd

from src.data_handler.data_handler import read_generated_csv
from src.definitions import GENERATED_DIR, RESULTS_DIR
from src.methods.dws import DWS
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.ita import ITA
from src.methods.method import Method
from src.methods.mk import MannKendall
from src.methods.splines import Splines
from src.methods.theil import Theil


def trend_detection_comparison(methods_list: List[Method], file_prefix: str,
                               folder: str = GENERATED_DIR) -> pd.DataFrame:
    """
    Search for all the files in the folder, then perform the detection

    :param methods_list: list with the methods that will perform the detection
    :param file_prefix: prefix of the files that will be used
    :param folder: folder that will contain the files. Default: data/generated_data
    :return: table with the results of the different methods and results
    """
    files = list()
    results = dict()
    columns = [method.name for method in methods_list]
    for file_path in glob.glob(f'{folder}/{file_prefix}*'):
        files.append(file_path)
    files.sort()  # sort by file name
    for file in files:
        name = file.split('/')[-1]
        x, y, trend, seasonality, noise = read_generated_csv(file)
        file_results = list()
        for method in methods_list:
            result = method.detect_trend(x, y)
            file_results.append(result)
        results[name] = file_results
    table = pd.DataFrame(results, columns)
    time = datetime.now()
    timestamp = f'{str(time.hour)}-{str(time.minute)}-{str(time.second)}-{str(time.microsecond)}'
    table.to_csv(f'{RESULTS_DIR}/trend_detection_{file_prefix}_{timestamp}.csv')
    return table


if __name__ == '__main__':
    methods_detection = [MannKendall(), ITA(), Theil(), DWS(), EmpiricalModeDecomposition(),
                         HPfilter(), Splines()]

    trend_detection_comparison(methods_detection, 'func')
