"""
A script for the preparation stage of the DVC pipeline.
"""

# imports
import os
import sys
import yaml
import dvc.api
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


# set up paths and helper scripts
sys.path.append('.')
sys.path.append('..')
sys.path.insert(1, '../scripts/')
import defaults as defs
import dataCleaner as dc
import dataVisualizer as dv
params = yaml.safe_load(open('params.yaml'))['preparation']
# setup helper scripts
cleaner = dc.dataCleaner(params['fromThe'])
visualizer = dv.dataVisualizer(params['fromThe'])


# read data using dvc
version = params['version']
# data path using dvc api
data_url = dvc.api.get_url(path = defs.path, 
                           #repo = defs.repo,
                           rev = version)
# reading the csv file using the dvc api
missing_values = params['missing_values']
df = pd.read_csv(data_url, na_values=missing_values)
print(df)


print(f'shape: {df.shape}, size: {df.size}')
print(df.info())
print(f'duplicates: {df.duplicated().value_counts()}')
print(df.isna().sum())
print(df.describe())


# convert the date time feature into a datetime object
df['date'] = pd.to_datetime(df['date'], errors='raise')
df.info()

# save the data to file
df.to_csv(defs.local_path, index=False)
print('prepared file saved successfully')
print('over and out')
