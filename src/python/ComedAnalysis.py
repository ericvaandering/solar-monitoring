#! /usr/bin/env python3
import os

import matplotlib.pyplot as plt
import pandas as pd

comed_directory = os.getenv('COMED_DATA_DIRECTORY')

comed_df = pd.read_feather(comed_directory + '/' + 'comed.ft')

# Split on March 16 when delivery DTOD started
early_df = comed_df[comed_df['Timestamp'] < 1773622800].copy()
late_df = comed_df[comed_df['Timestamp'] >= 1773622800].copy()

tmp_view = comed_df
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.hour)]).mean()

tmp_early = early_df
tmp_early.drop('Date', axis=1, inplace=True)
early_view = tmp_early.groupby([(tmp_early.index.hour)]).mean()

tmp_late = late_df
tmp_late.drop('Date', axis=1, inplace=True)
late_view = tmp_late.groupby([(tmp_late.index.hour)]).mean()

plt.clf()
year_view['Supply price'].plot()
plt.title('Average supply price')
plt.xlabel("Hour")
plt.ylabel("(¢/kWh)")
plt.savefig('ComEd supply hourly average.pdf', bbox_inches='tight')

plt.clf()
year_view['Total price'].plot()
plt.title('Average total price')
plt.xlabel("Hour")
plt.ylabel("(¢/kWh)")
plt.savefig('ComEd price hourly average.pdf', bbox_inches='tight')

plt.clf()
early_view['Total price'].plot()
plt.title('Average total price before DTOD')
plt.xlabel("Hour")
plt.ylabel("(¢/kWh)")
plt.savefig('ComEd early hourly average.pdf', bbox_inches='tight')

plt.clf()
late_view['Total price'].plot()
plt.title('Average total price after DTOD')
plt.xlabel("Hour")
plt.ylabel("(¢/kWh)")
plt.savefig('ComEd late hourly average.pdf', bbox_inches='tight')
