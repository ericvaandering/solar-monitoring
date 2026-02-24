#! /usr/bin/env python3
import datetime
import json
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

enphase_directory = os.getenv('ENPHASE_DATA_DIRECTORY')
comed_directory = os.getenv('COMED_DATA_DIRECTORY')
# Get delivery cost info
delivery_costs = json.load(open('../../containers/Analysis/delivery.json'))

# Read in raw data from ComEd
py_array = []
files = glob.glob(comed_directory + '????-??-??_comed.json')
for comed_file in files:
    print(f'Processing {comed_file}')
    month_comed = json.load(open(comed_file))
    for ts in month_comed.keys():
        py_array.append([int(ts), month_comed[ts]])
comed_np = np.array(py_array)

# Read in RAW data from Emporia

# Do multiples like this
# dfs = [] # an empty list to store the data frames
#
# for file in file_list:
#     # Use pd.read_json() to read the file.
#     # If your files are JSON Lines format, use lines=True.
#     # You may also need to use pd.json_normalize() for nested JSON structures.
#     data = pd.read_json(file, lines=True)
#     dfs.append(data) # append the data frame to the list
#
# # Concatenate all the data frames in the list into a single DataFrame
# merged_df = pd.concat(dfs, ignore_index=True)

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html with keep

comed_df = pd.DataFrame(comed_np, columns=['Timestamp', 'Supply Price'])
comed_df['Timestamp'] = comed_df['Timestamp'].astype(int)
local_timezone = 'US/Central'
# Add additional time/data columns to power2
comed_df['Time'] = pd.to_datetime(comed_df['Timestamp'], unit='s')
comed_df['Date'] = comed_df['Time'].map(lambda x: x.date())
comed_df['AwareTime'] = comed_df['Time'].dt.tz_localize('UTC')
comed_df['LocalTime'] = comed_df['AwareTime'].dt.tz_convert(local_timezone)
comed_df.set_index('LocalTime', inplace=True)

# Add delivery cost info to table
comed_df = comed_df.assign(Delivery=0.065)  # Default value FIXME: make it an average
#power2 = power2.assign(Delivery=0.065)  # Default value FIXME: make it an average
for bill in delivery_costs:
    start = datetime.datetime.fromisoformat(bill['start']).date()
    end = datetime.datetime.fromisoformat(bill['end']).date()
    charge = bill['charge']
    # Fill it in, leaves unchanged if the date does not match
    comed_df['Delivery'] = np.where((comed_df['Date'] <= end) & (comed_df['Date'] >= start), bill['charge'],
                                 comed_df['Delivery'])
    # power2['Delivery'] = np.where((power2['Date'] <= end) & (power2['Date'] >= start), bill['charge'],
    #                               power2['Delivery'])
tmp_view = comed_df
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.hour)]).mean()
year_view['Supply Price'].plot()

import pdb; pdb.set_trace()

# Prices are in cents/kWh, values are in Wh (or watts?)
# power['Generated Cost'] = (power['Delivery'] + power['Supply Price'] / 100) * power['Generated'] / 1000
# power['Consumed Cost'] = (power['Delivery'] + power['Supply Price'] / 100) * power['Consumed'] / 1000
# power['EV Cost'] = (power['Delivery'] + power['Supply Price'] / 100) * power['EV Charger'] / 1000
# power2['Generated Cost'] = (power2['Delivery'] + power2['Supply Price'] / 100) * power2['Generated'] / 1000
# power2['Consumed Cost'] = (power2['Delivery'] + power2['Supply Price'] / 100) * power2['Consumed'] / 1000
# power2['EV Cost'] = (power2['Delivery'] + power2['Supply Price'] / 100) * power2['EV Charger'] / 1000

print(power)
print(power['Generated Cost'].sum())
# print(power2['Generated Cost'].sum())

month_view = power.groupby('Date').sum()
print(month_view)

tmp_view = power
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.year), (tmp_view.index.month)]).sum()
year_view.index.names = ['Year', 'Month']
print(year_view)

month_view['Generated Cost'].plot(title='Generated Value per Day', ylabel='Dollars', rot=-45)
plt.tight_layout()
plt.savefig('DayValue.pdf', bbox_inches='tight')

plt.clf()
(month_view['Generated'] / 1000).plot(title='Generated Power per Day', ylabel='kWh', xlabel='Date', rot=-45)
plt.tight_layout()
plt.savefig('DayPower.pdf', bbox_inches='tight')

# Plot the yearly as a bar plot

df_plot = year_view.groupby(['Year', 'Month']).sum()

df_plot.plot(kind='bar', y='Generated Cost', legend=False)
plt.xlabel('Year and Month')
plt.ylabel('Generated Value ($)')
plt.title('Value Generated per Month')
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.savefig('MonthValue.pdf', bbox_inches='tight')

df_plot['Generated'] = df_plot['Generated'] / 1000
df_plot.plot(kind='bar', y='Generated', legend=False, rot=45)
plt.xlabel('Year and Month')
plt.ylabel('kWh')
plt.title('kWh Generated per Month')
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.savefig('MonthPower.pdf', bbox_inches='tight')

import pdb; pdb.set_trace()
