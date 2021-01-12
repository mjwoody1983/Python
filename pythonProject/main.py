# This is a standard loader for betting data

import os
import pandas as pd
from urllib.request import urlopen
from scipy import stats
import warnings
from dotenv import load_dotenv


load_dotenv()


warnings.filterwarnings('ignore')

# *********************************************************** #
# Load data into model for different functions
# *********************************************************** #

# Load the fixture for the current week
fd_fix = urlopen('https://www.football-data.co.uk/fixtures.csv')

# Add all potential leagues to the model
filesLoad = ['e0.csv', 'e1.csv', 'e2.csv', 'e3.csv', 'ec.csv', 'b1.csv', 'd2.csv', 'f1.csv', 'f2.csv',
             'n1.csv', 'p1.csv', 'sc0.csv', 'sc1.csv', 'sc2.csv', 'sc3.csv', 'sp2.csv', 't1.csv',
             'd1.csv', 'sp1.csv', 'i1.csv', 'i2.csv', 'g1.csv']

# Current league url:
league_path = 'https://www.football-data.co.uk/mmz4281/2021/'

# Will append the dataframes from below into list_.
list_ = []

for files in filesLoad:
    fd = urlopen(league_path + files)
    df = pd.read_csv(fd, sep=",", encoding='cp1252')
    list_.append(df)

frame = pd.concat(list_)

fix_df = pd.read_csv(fd_fix)

print(fix_df)

for col in fix_df.columns:
    print(col)

# Save file to tmp folder
path_set = 'C://tmp//'
frame.to_csv(path_set + 'results_this_season_.csv', index=False, line_terminator='\n')
