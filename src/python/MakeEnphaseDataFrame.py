#! /usr/bin/env python3
import glob
import json
import os

import pandas as pd

local_timezone = 'US/Central'

enphase_directory = os.getenv('ENPHASE_DATA_DIRECTORY')

# Read in raw data from Enphase
data_list = []
files = glob.glob(enphase_directory + '????-??-??.json')
for enphase_file in files:
    print(f'Processing {enphase_file}')
    month_enphase = json.load(open(enphase_file))
    for ts in month_enphase.keys():
        new_row_data = {'Timestamp': int(ts), 'Consumed': month_enphase[ts]['wh_consumed'],
                        'Generated': month_enphase[ts].get('wh_generated', 0)}
        data_list.append(new_row_data)

enphase_df = pd.DataFrame(data_list)

# Add additional time/data columns
enphase_df['Time'] = pd.to_datetime(enphase_df['Timestamp'], unit='s')
enphase_df['LocalTime'] = (pd.to_datetime(enphase_df['Timestamp'], unit='s', utc=True)
                           .dt.tz_convert(local_timezone))
enphase_df['Date'] = enphase_df['LocalTime'].map(lambda x: x.date())
enphase_df.set_index('LocalTime', inplace=True)

# Normalize to kW and integer timestamp
enphase_df['Timestamp'] = enphase_df['Timestamp'].astype(int)
enphase_df['Consumed'] = enphase_df['Consumed'] / 1000.0
enphase_df['Generated'] = enphase_df['Generated'] / 1000.0

enphase_df.to_feather('enphase.ft')
print(enphase_df)
