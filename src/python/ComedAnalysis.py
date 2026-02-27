#! /usr/bin/env python3
import os

import matplotlib.pyplot as plt
import pandas as pd

comed_directory = os.getenv('COMED_DATA_DIRECTORY')

comed_df = pd.read_feather(comed_directory + '/' + 'comed.ft')

tmp_view = comed_df
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.hour)]).mean()

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
