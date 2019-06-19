import random
import numpy as np
import configparser
import pandas as pd

from src.data_handler.data_handler import *
from src.definitions import *


from src.compare_functions import trend_estimation_comparison
from src.data_handler import data_handler
from src.methods.dws import DWS
from src.methods.emd import EmpiricalModeDecomposition
from src.methods.hp_filter import HPfilter
from src.methods.ita import ITA
from src.methods.lowess import Lowess
from src.methods.mk import MannKendall
from src.methods.regression import Regression
from src.methods.splines import Splines
from src.methods.theil import Theil


def generate_with_name(file_name: str, num_files: int):
    for i in range(num_files):
        name = f'/{file_name}_{str(i + 1)}.ini'
        generate_synthetic_data('function', name)


# Generate time series with trend, seasonality and noise
def generate_data(data_points: int = 300,
                  sig_noise_ratio: list = np.linspace(0, 3, 10)):

    # Alternatives for seasonalities, with 3 components increasing in frequency and decreasing in amplitude.
    seasonalities: list = [ 'np.random.uniform(size=1)*1*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*10+1)+(np.random.uniform(size=1)*2*np.pi))'\
                            + '+np.random.uniform(size=1)*0.5*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*20+1)+(np.random.uniform(size=1)*2*np.pi))'\
                            + '+np.random.uniform(size=1)*0.25*np.sin((y*2*np.pi)*(np.random.uniform(size=1)*50+1)+(np.random.uniform(size=1)*2*np.pi))' \
                            for x in range(10)]

    # generate trend functions:
    # 12 structures
    trend_structures: list = [
        'a*x**0',
        'a*x**1',
        'a*x**2',
        'a*x**3',
        'a*(x+1)**-3',
        'a*x**(1/2)',
        'a*x**(1/3)',
        'a*x**3 - a*x**2',
        'a*x**5 - a*x**2 + a*x',
        'a*np.sin((x*2*np.pi)/(b*2+1) + c*np.pi)',
        'a*5**x'
    ]

    trends_synthetic: list = np.empty([0, len(trend_structures)])

    coefficients = np.empty([0, 3])

    # This is done to remember what random values were set for the coefficients.
    for i in range(30):
        a, b, c = np.random.uniform(),  np.random.uniform(),  np.random.uniform()

        # Add coefficients
        trend_set = np.copy(trend_structures)
        trend_set = np.core.defchararray.replace(trend_set, 'a', str(a))
        trend_set = np.core.defchararray.replace(trend_set, 'b', str(b))
        trend_set = np.core.defchararray.replace(trend_set, 'c', str(c))

        trends_synthetic = np.append(trends_synthetic, [trend_set], axis=0)
        coefficients = np.append(coefficients, [[a, b, c]], axis=0)

    trends_pseudoreal: list = [
        ['monthly', 'Date', 'Price', 833],
        ['brent-daily_csv', 'time', 'price', 8131],
        ['data_csv_index', 'time', 'index', 1768],
        ['data_csv_price', 'time', 'price', 1768],
        ['data_csv_sp500', 'time', 'sp500', 1768],
        ['economics_pce', 'time', 'pce', 574],
        ['economics_unemploy', 'time', 'unemploy', 574],
        ['maastricht_temp', 'time', 'temp', 153],
        ['marathon', 'time', 'time_marathon', 120],
        ['monthly_csv', 'time', 'price', 833],
        ['number_flight_guests_sysdney_melbourn', 'time', 'number_of_guests', 282],
        ['vix-daily_csv', 'time', 'score', 3885],
        ['weather_aachen', 'time', 'QN', 500],
        ['wti-daily_csv', 'time', 'price', 8424]
    ]

    index_synthetic = 0
    index_pseudoreal = 0
    for noise in sig_noise_ratio:
        for seasonality in seasonalities:
            for i in range(len(trends_synthetic)):
                for j in range(len(trends_synthetic[i])):
                    trend = trends_synthetic[i][j]
                    index_synthetic += 1
                    # create .ini function file
                    create_function_file_synthetic('synthetic' + str(index_synthetic), trend, data_points, noise, seasonality, coefficients[i], trend_structures[j])
                    # create .csv data file
                    generate_synthetic_data('function', 'synthetic' + str(index_synthetic) + '.ini')
            index_pseudoreal += 1
            for i in range(len(trends_pseudoreal)):
                trend = trends_pseudoreal[i]
                # create .ini function file
                create_function_file_pseudoreal(index_pseudoreal, trend[0], True, trend[1], trend[2], 'db8', trend[3], noise, seasonality)
                # create .csv function file
                generate_synthetic_data('data', trend[0] + str(index_pseudoreal) + '.ini')


def obtain_config(config_file_name: str) -> configparser.ConfigParser:
    """
    Read the config file

    :param config_file_name: name of the file
    :return: parameters in the config file
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config_file_path = SYNTHETIC_DIR + '/' + config_file_name
    config.read(config_file_path)
    return config


if __name__ == '__main__':
    generate_data()

    methods_detection = [ITA(), MannKendall(), Regression(), Theil()]
    methods_estimation = [EmpiricalModeDecomposition(), HPfilter(), Splines(), Theil(), Regression(), Lowess()]

    trend_estimation_comparison(methods_estimation, '*')
    #generate_with_name('func', 5)
