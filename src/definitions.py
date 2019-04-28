import sys
from os.path import dirname, abspath

# Definitions of some path to avoid problems in the execution
SOURCE_DIR = dirname(abspath(__file__))
ROOT_DIR = dirname(SOURCE_DIR)
DATA_DIR = ROOT_DIR + '/data/'
SYNTHETIC_DIR = DATA_DIR + '/synthetic/'

# This add the root, so the everything can be executed from the terminal
sys.path.append(ROOT_DIR)



