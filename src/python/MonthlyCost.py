#! /usr/bin/env python3
import os

import matplotlib.pyplot as plt
import pandas as pd

enphase_directory = os.getenv('ENPHASE_DATA_DIRECTORY')
comed_directory = os.getenv('COMED_DATA_DIRECTORY')

emporia_df = pd.read_feather(enphase_directory + '/' + 'emporia.ft')
enphase_df = pd.read_feather(enphase_directory + '/' + 'enphase.ft')
comed_df = pd.read_feather(comed_directory + '/' + 'comed.ft')

power = pd.merge(enphase_df, comed_df, on='LocalTime', how='inner').merge(emporia_df, on='LocalTime', how='inner')
power2 = pd.merge(enphase_df, comed_df, on='LocalTime', how='outer').merge(emporia_df, on='LocalTime', how='outer')

power.drop(columns=['Timestamp_x', 'Time_x', 'Date_x', 'Timestamp_y', 'Time_y', 'Date_y'], inplace=True)
power2.drop(columns=['Timestamp_x', 'Time_x', 'Date_x', 'Timestamp_y', 'Time_y', 'Date_y'], inplace=True)


# Prices are in cents/kWh, values are in kWh (or watts?)
power['Generated Cost'] = (power['Delivery'] + power['Supply price']) * power['Generated']
power['Consumed Cost'] = (power['Delivery'] + power['Supply price']) * power['Consumed']
power['EV Cost'] = (power['Delivery'] + power['Supply price']) * power['EV Charger']
power2['Generated Cost'] = (power2['Delivery'] + power2['Supply price']) * power2['Generated']
power2['Consumed Cost'] = (power2['Delivery'] + power2['Supply price']) * power2['Consumed']
power2['EV Cost'] = (power2['Delivery'] + power2['Supply price']) * power2['EV Charger']

print(power)
print(f'Generated value ' + str(power['Generated Cost'].sum()))
print(f'Generated value 2 ' + str(power2['Generated Cost'].sum()))

tmp_view = power2.drop(columns=['Timestamp', 'Time', ])
month_view = tmp_view.groupby('Date').sum()
print(month_view)

tmp_view = power2.drop(columns=['Timestamp', 'Time', 'Date'])
year_view = tmp_view.groupby([(tmp_view.index.year), (tmp_view.index.month)]).sum()
year_view.index.names = ['Year', 'Month']
print(year_view)

# Good until here
# FIXME: Also drop price columns as they make no sense

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
