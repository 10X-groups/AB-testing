"""
A script for the preparation stage of the DVC pipeline.
"""

# imports
import os
import sys
import dvc.api
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
import yaml

# set up paths and helper scripts
"""sys.path.append('.')
sys.path.insert(1, '../scripts/')

import defaults as defs
import dataCleaner as dc
import dataVisualizer as dv"""

params = yaml.safe_load(open('params.yaml'))['preparation']

# setup helper scripts
cleaner = dataCleaner(params['fromThe'])
visualizer = dataVisualizer(params['fromThe'])

