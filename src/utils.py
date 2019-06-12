from datetime import datetime
from typing import Tuple

import pandas as pd


def generate_timestamp() -> str:
    """
    Generates a string with the timestamp to append to the file name.

    :return: string with a unique timestamp
    """
    time = datetime.now()
    return f'{str(time.hour)}-{str(time.minute)}-{str(time.second)}-{str(time.microsecond)}'


def read_generated_csv(file_path: str) -> Tuple:
    """
    Method that simplifies the read of a generated csv file to work with the
    system

    :param file_path: complete path for the csv to read
    :return: Tuple with the numpy arrays for x, y, trend, seasonality and noise
    """
    data = pd.read_csv(file_path)
    x = data.x.to_numpy()
    y = data.y.to_numpy()
    trend = data.trend.to_numpy()
    seasonality = data.seasonality.to_numpy()
    noise = data.noise.to_numpy()
    return x, y, trend, seasonality, noise


def get_name_from_path(path: str, extension: bool = False) -> str:
    """
    Method that returns the name of the file given the full path of it

    :param path: full path of the file in a string
    :param extension: flag to keep the extension of the file
    :return: name of the file in a string
    """
    name = path.split('/')[-1]
    if not extension:
        name = name.split('.')[0]
    return name