import sys
from os.path import dirname, abspath

# Definitions of some path to avoid problems in the execution
SOURCE_DIR = dirname(abspath(__file__))
ROOT_DIR = dirname(SOURCE_DIR)
DATA_DIR = ROOT_DIR + '/data'
RESULTS_DIR = ROOT_DIR + '/results'
SYNTHETIC_DIR = DATA_DIR + '/synthetic'
GENERATED_DIR = DATA_DIR + '/generated_data'
PLOTS_DIR = DATA_DIR + '/plots_estimation'

# Name definitions for the data handler

TREND_DATA = 'trend'
NOISE_DATA = 'noise'
SEASONALITY_DATA = 'seasonality'
FILE_DATA = 'file'
SAVE_DATA = 'save'

# Properties of the data handler

FILE_NAME = 'filename'
HEADER = 'header'
X_COL = 'x_column'
Y_COL = 'y_column'
WAVELET = 'wavelet'
LEVELS = 'levels'
FUNC = 'function'
DATA_PTS = 'data_points'
SIGNAL_TO_NOISE = 'signal_to_noise'

MATLAB = '.mat'
CSV = '.csv'


# This add the root, so the everything can be executed from the terminal
sys.path.append(ROOT_DIR)
