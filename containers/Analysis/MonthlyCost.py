#! /usr/bin/env python3
import datetime
import json
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# FIXME: Read all files with the pattern
# FIXME: Read all comed files

# Get delivery cost info
delivery_costs = json.load(open('delivery.json'))

# Read in raw data from Enphase
py_array = []
files = glob.glob('????-??-??.json')
for enphase_file in files:
    print(f'Processing {enphase_file}')
    month_enphase = json.load(open(enphase_file))
    for ts in month_enphase.keys():
        py_array.append([int(ts), month_enphase[ts]['wh_consumed'], month_enphase[ts].get('wh_generated',0)])
enphase_np = np.array(py_array)

# Read in raw data from ComEd
py_array = []
files = glob.glob('????-??-??_comed.json')
for comed_file in files:
    print(f'Processing {comed_file}')
    month_comed = json.load(open(comed_file))
    for ts in month_comed.keys():
        py_array.append([int(ts), month_comed[ts]])
comed_np = np.array(py_array)

# Build and merge dataframes based on timestamp
enphase_df = pd.DataFrame(enphase_np, columns=['Timestamp', 'Consumed', 'Generated'])
comed_df = pd.DataFrame(comed_np, columns=['Timestamp', 'Supply Price'])
power = pd.merge(enphase_df, comed_df, on='Timestamp', how='inner')

# Add additional time/data columns
power['Time'] = pd.to_datetime(power['Timestamp'], unit='s')
power['Date'] = power['Time'].map(lambda x: x.date())
power.set_index('Time', inplace=True)

# Add delivery cost info to table
power = power.assign(Delivery=0.09)  # Default value FIXME: make it an average
for bill in delivery_costs:
    start = datetime.datetime.fromisoformat(bill['start']).date()
    end = datetime.datetime.fromisoformat(bill['end']).date()
    charge = bill['charge']
    # Fill it in, leaves unchanged if the date does not match
    power['Delivery'] = np.where((power['Date'] <= end) & (power['Date'] >= start), bill['charge'],
                                 power['Delivery'])

# Prices are in cents/kWh, values are in Wh (or watts?)
power['Generated Cost'] = (power['Delivery'] + power['Supply Price'] / 100) * power['Generated'] / 1000
power['Consumed Cost'] = (power['Delivery'] + power['Supply Price'] / 100) * power['Consumed'] / 1000
print(power)
print(power['Generated Cost'].sum())

month_view = power.groupby('Date').sum()
print(month_view)


tmp_view = power
tmp_view.drop('Date', axis=1, inplace=True)
year_view =tmp_view.groupby([(tmp_view.index.year), (tmp_view.index.month)]).sum()
year_view.index.names = ['Year', 'Month']
print(year_view)

month_view['Generated Cost'].plot(title='Generated Value per Day', ylabel='Dollars', rot=-45)
plt.tight_layout()
plt.show()

(month_view['Generated'] / 1000).plot(title='Generated Power per Day', ylabel='kWh', rot=-45)
plt.tight_layout()
plt.show()

# Plot the yearly as a bar plot

df_plot = year_view.groupby(['Year', 'Month']).sum()
print(df_plot)

df_plot.plot(kind='bar', y='Generated Cost', legend=False)
plt.xlabel('Year and Month')
plt.ylabel('Generated Value ($)')
plt.title('Value Generated per Month')
plt.xticks(rotation=45) # Rotate labels for better readability
plt.tight_layout() # Adjust layout to prevent clipping of labels
plt.show()

df_plot['Generated'] = df_plot['Generated'] / 1000
df_plot.plot(kind='bar', y='Generated', legend=False, rot=45)
plt.xlabel('Year and Month')
plt.ylabel('kWh')
plt.title('kWh Generated per Month')
plt.tight_layout() # Adjust layout to prevent clipping of labels
plt.show()
