#! /usr/bin/env python3

import datetime
import glob
import json
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

local_timezone = 'US/Central'

comed_directory = os.getenv('COMED_DATA_DIRECTORY')
# Get delivery cost info supplied as part of the container
delivery_costs = json.load(open('/delivery.json'))


def dtod(start_day, end_day, dtod_prices):
    prices = []
    current = start_day
    while current <= end_day:
        current += datetime.timedelta(days=1)

        for range, price in dtod_prices.items():
            start_hour, end_hour = range.split('-')
            start_time = (datetime.datetime.combine(current, datetime.time(int(start_hour), 0, 0))
                          + datetime.timedelta(seconds=1))
            if end_hour == '24':
                end_time = datetime.datetime.combine(current, datetime.time(23, 59, 59))
            else:
                end_time = datetime.datetime.combine(current, datetime.time(int(end_hour), 0, 0))

            start_ts = start_time.replace(tzinfo=ZoneInfo(local_timezone)).timestamp()
            end_ts = end_time.replace(tzinfo=ZoneInfo(local_timezone)).timestamp()
            prices.append((int(start_ts), int(end_ts), price))

    return prices


data_list = []

# Read in raw data from ComEd files
files = glob.glob(comed_directory + '????-??-??_comed.json')
for comed_file in files:
    print(f'Processing {comed_file}')
    month_comed = json.load(open(comed_file))
    for ts in month_comed.keys():
        new_row_data = {'Timestamp': int(ts), 'Supply price': month_comed[ts]}
        data_list.append(new_row_data)

comed_df = pd.DataFrame(data_list)

# Add additional time/data columns
comed_df['Time'] = pd.to_datetime(comed_df['Timestamp'], unit='s')
comed_df['LocalTime'] = (pd.to_datetime(comed_df['Timestamp'], unit='s', utc=True)
                         .dt.tz_convert(local_timezone))
comed_df['Date'] = comed_df['LocalTime'].map(lambda x: x.date())
comed_df.set_index('LocalTime', inplace=True)

# Normalize to dollars and integer timestamp
comed_df['Timestamp'] = comed_df['Timestamp'].astype(int)
comed_df['Supply price'] = comed_df['Supply price'] / 100.0

# Add delivery cost info to dataframe
comed_df = comed_df.assign(Delivery=0.065)  # Default value FIXME: make it an average
for bill in delivery_costs:
    start = datetime.datetime.fromisoformat(bill['start']).date()
    end = datetime.datetime.fromisoformat(bill['end']).date()
    if 'charge' in bill:
        charge = bill['charge']
        # Fill it in, leaves unchanged if the date does not match
        comed_df['Delivery'] = np.where((comed_df['Date'] <= end) & (comed_df['Date'] >= start), charge,
                                        comed_df['Delivery'])
    elif 'dtod' in bill:
        for (start_time, end_time, delivery) in dtod(start, end, bill['dtod']):
            # Fill it in, leaves unchanged if the timestamp does not match
            comed_df['Delivery'] = np.where((comed_df['Timestamp'] <= end_time) & (comed_df['Timestamp'] >= start_time),
                                            delivery, comed_df['Delivery'])

comed_df['Total price'] = comed_df['Delivery'] + comed_df['Supply price']

# Split on March 16 when delivery DTOD started
early_df = comed_df[comed_df['Timestamp'] < 1773622800].copy()
late_df = comed_df[comed_df['Timestamp'] >= 1773622800].copy()

comed_df.to_feather('comed.ft')
early_df.to_feather('comed_early.ft')
late_df.to_feather('comed_late.ft')
