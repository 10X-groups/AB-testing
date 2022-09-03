"""A script to compress csv files."""

# imports
import sys
import dvc.api
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

# setting up logger
from loggerImporter import setup_logger
logger= setup_logger('logs/compress_root.log')
logger.info(f'created a data compressor logger for compress.py file.')

# set up paths and helper scripts
sys.path.append('.')
sys.path.insert(1, '../scripts/')
from defaults import *

# read data using dvc
#version = 'v1'

# data path using dvc api
data_url = dvc.api.get_url(path = 'data/ABtwoCampaignEngView.csv')
logger.info(f'obtained the data url: {data_url}')

# reading the data
missing_values = ["n/a", "na", "undefined", '?', 'NA', 'undefined']
df = pd.read_csv(data_url, na_values=missing_values)
logger.info(f'obtained the data {df.shape} from the data url: {data_url}')

# compress and save the original dataset
df.to_csv('../'+data_path + second_data_file + '.bz2', index=False)
logger.info(f'file compressed and saved successfully to {data_path + second_data_file + ".bz2"}')
print(f'file compressed and saved successfully to {data_path + second_data_file + ".bz2"}')


"""new_df = pd.read_csv('data/ABtwoCampaignEngView.csv')
new_df.info()
#new_df.drop(['Unnamed: 0'], axis=1, inplace=True)
new_df.info()
new_df.to_csv('data/ABtwoCampaignEngView.csv', index=False)"""