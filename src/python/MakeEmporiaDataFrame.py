#! /usr/bin/env python3
import glob
import json
import os
import pdb

import pandas as pd

local_timezone = 'US/Central'

emporia_directory = os.getenv('ENPHASE_DATA_DIRECTORY')

emporia_history_file = emporia_directory + '/history_emporia.json'
data_list = json.load(open(emporia_history_file))
print(f'From history file: {len(data_list)} datapoints')

# Read in raw data from Enphase monthly reports
files = glob.glob(emporia_directory + '/????-??_emporia.json')
for enmporia_file in files:
    month_emporia = json.load(open(enmporia_file))
    data_list.extend(month_emporia)
    print(f'Processed {enmporia_file}: {len(data_list)} datapoints')

# Build and merge dataframes based on timestamp
# enphase_df = pd.DataFrame(enphase_np, columns=['Timestamp', 'Consumed', 'Generated'])
emporia_df = pd.DataFrame(data_list)
emporia_df['Timestamp'] = emporia_df['Timestamp'].astype(int)

print(f'Before dropping duplicates: {len(emporia_df)} datapoints')

emporia_df.drop_duplicates(subset=['Timestamp'], keep='last', inplace=True)
print(f'After dropping duplicates: {len(emporia_df)} datapoints')

# Add additional time/data columns
emporia_df['Time'] = pd.to_datetime(emporia_df['Timestamp'], unit='s')
emporia_df['LocalTime'] = (pd.to_datetime(emporia_df['Timestamp'], unit='s', utc=True)
                           .dt.tz_convert(local_timezone))
emporia_df['Date'] = emporia_df['LocalTime'].map(lambda x: x.date())
emporia_df.set_index('LocalTime', inplace=True)

# Normalize to kW and integer timestamp
emporia_df['Timestamp'] = emporia_df['Timestamp'].astype(int)
emporia_df['EV Charger'] = emporia_df['EV Charger'] / 1000.0

emporia_df.to_feather('emporia.ft')
print(emporia_df)
print(emporia_df['EV Charger'].max())
