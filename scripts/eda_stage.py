"""
A script for the eda stage of the DVC pipeline.
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


print('\ninitializing helper scripts and dependencies . . .\n')
# set up paths and helper scripts
sys.path.append('.')
sys.path.append('..')
sys.path.insert(1, '../scripts/')
import defaults as defs
import dataCleaner as dc
import dataVisualizer as dv
params = yaml.safe_load(open('params.yaml'))['eda']
# setup helper scripts
cleaner = dc.dataCleaner(params['fromThe'])
visualizer = dv.dataVisualizer(params['fromThe'])


print('\nloading data . . .\n')
# read data using dvc
version = params['version']
# data path using dvc api
data_url = dvc.api.get_url(path = defs.data_path + params['dataFileName'], 
                           #repo = defs.repo,
                           rev = version)
# reading the csv file using the dvc api
missing_values = params['missing_values']
df = pd.read_csv(data_url, na_values=missing_values)
print(df)


print('\ndisplay basic metadata information . . .\n')
print(f"---> file name: {params['dataFileName']}\n" +
      f"---> file version: {params['version']}\n" +
      f"---> missing values used: {params['missing_values']}\n" +
      f"---> running script: {params['fromThe']}")


print('\ndisplay basic information . . .\n')















print('\nsaving explored and modified data . . .\n')
# save the data to file
df.to_csv(defs.data_path + params['dataFileName'], index=False)
print('explored and modified data file saved successfully')
print('over and out')