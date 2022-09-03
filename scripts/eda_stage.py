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
print(f'shape: {df.shape}, size: {df.size}')
print(df.info())
print(df.describe())


print('\ndisplay univariate analysis . . .\n')
print(f'number of auction id:\n{df["auction_id"].nunique()}')
print(f"Experiment groups:\n{df['experiment'].value_counts()}")
visualizer.plot_count(df, 'experiment', save_as = defs.plot_path+'eda-fig-experiment.png')

print(f"date groups:\n{df['date'].value_counts()}")
visualizer.plot_count(df, 'date', save_as = defs.plot_path+'eda-fig-date.png')

print(f"hour groups:\n{df['hour'].value_counts()}")
visualizer.plot_count(df, 'hour', save_as = defs.plot_path+'eda-fig-hour.png')

print(f"device make groups:\n{df['device_make'].value_counts()}")
visualizer.plot_pie(df, 'device_make', save_as = defs.plot_path+'eda-fig-device-make.png')

print(f"browser groups:\n{df['browser'].value_counts()}")
visualizer.plot_count(df, 'browser', save_as = defs.plot_path+'eda-fig-browser.png')

print(f"yes groups:\n{df['yes'].value_counts()}")
visualizer.plot_count(df, 'yes', save_as = defs.plot_path+'eda-fig-yes.png')

print(f"no groups:\n{df['no'].value_counts()}")
visualizer.plot_count(df, 'no', save_as = defs.plot_path+'eda-fig-no.png')


print('\nplot bivariate analysis graphs to plots folder . . .\n')
visualizer.plot_count(df, 'date', 'experiment', 'experiment vs date', save_as = defs.plot_path+'eda-fig-exp-date.png')
visualizer.plot_count(df, 'hour', 'experiment', 'experiment vs hour', save_as = defs.plot_path+'eda-fig-exp-hour.png')
visualizer.plot_count(df, 'browser', 'experiment', 'experiment vs browser', save_as = defs.plot_path+'eda-fig-exp-browser.png')
visualizer.plot_count(df, 'yes', 'experiment', 'experiment vs yes', save_as = defs.plot_path+'eda-fig-exp-yes.png')
visualizer.plot_count(df, 'no', 'experiment', 'experiment vs no', save_as = defs.plot_path+'eda-fig-exp-no.png')


print('\ndisplay control vs exposed BIO participants percentage . . .\n')
participation_counts = df.groupby(['experiment']).agg({'yes': 'sum', 'no': 'sum'})
print(participation_counts)


control_participants_yes = participation_counts.loc[participation_counts.index == 'control']['yes'].values[0]
control_participants_no =  participation_counts.loc[participation_counts.index == 'control']['no'].values[0]
control_participants = control_participants_yes + control_participants_no
exposed_participants_yes = participation_counts.loc[participation_counts.index == 'exposed']['yes'].values[0]
exposed_participants_no =  participation_counts.loc[participation_counts.index == 'exposed']['no'].values[0]
exposed_participants = exposed_participants_yes + exposed_participants_no
print(f'control group BIO participants: {control_participants}\nexposed group BIO participants: {exposed_participants}')


control_not_participated = df.loc[df['experiment'] == 'control'][df['yes'] == 0][df['no'] == 0]
exposed_not_participated = df.loc[df['experiment'] == 'exposed'][df['yes'] == 0][df['no'] == 0]
print(f'control group BIO non participants: {control_not_participated.value_counts().sum()}\nexposed group BIO non participants: {exposed_not_participated.value_counts().sum()}')


control_participants_total_ratio = control_participants / df['experiment'].value_counts().values[0]
control_non_participants_total_ratio = control_not_participated.value_counts().sum() / df['experiment'].value_counts().values[0]
print("Control group BIO participants percentage: %.4f" %(control_participants_total_ratio*100))
print("Control group BIO non participants percentage: %.4f" %(control_non_participants_total_ratio*100))


exposed_participants_total_ratio = exposed_participants / df['experiment'].value_counts().values[1]
exposed_non_participants_total_ratio = exposed_not_participated.value_counts().sum() / df['experiment'].value_counts().values[1]
print("Exposed group BIO participants percentage: %.4f" %(exposed_participants_total_ratio*100))
print("Exposed group BIO non participants percentage: %.4f" %(exposed_non_participants_total_ratio*100))


participation_counts['total participants'] = [control_participants, exposed_participants]
participation_counts['total non participants'] = [control_not_participated.value_counts().sum(), exposed_not_participated.value_counts().sum()]
participation_counts['total number'] = [df['experiment'].value_counts().values[0], df['experiment'].value_counts().values[1]]
participation_counts['participants percentage'] = [control_participants_total_ratio*100, exposed_participants_total_ratio*100]
participation_counts['non participants percentage'] = [control_non_participants_total_ratio*100, exposed_non_participants_total_ratio*100]
print(participation_counts)
print(participation_counts.describe())


visualizer.plot_heatmap(df, 'Correlation of the numerical columns', save_as=defs.plot_path + 'eda-correlation.png')


print('\nsaving BIO participants data . . .')
# save the data to file
participation_counts.to_csv(defs.data_path + params['bioPercentage'], index=False)
print('BIO participants data file saved successfully')


print('\nsaving explored and modified data . . .')
# save the data to file
df.to_csv(defs.data_path + params['dataFileName'], index=False)
print('explored and modified data file saved successfully')
print('over and out')
