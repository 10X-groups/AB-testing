"""A script to compress csv files."""

# importing modules
import sys
import dvc.api
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

# set up paths and helper scripts
sys.path.append('.')
sys.path.insert(1, '../scripts/')
from defaults import *

# read data using dvc
version = 'v1'

# data path using dvc api
data_url = dvc.api.get_url(path = path, rev = version)

# reading the data
missing_values = ["n/a", "na", "undefined", '?', 'NA', 'undefined']
df = pd.read_csv(data_url, na_values=missing_values)


# compress and save the original data set
df.to_csv(path + '.bz2', index=False)
print('file compressed and saved successfully.')
