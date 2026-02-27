#! /usr/bin/env python3
import os

import matplotlib.pyplot as plt
import pandas as pd

enphase_directory = os.getenv('ENPHASE_DATA_DIRECTORY')

enphase_df = pd.read_feather(enphase_directory + '/' + 'enphase.ft')

tmp_view = enphase_df
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.hour)]).mean()

plt.clf()
year_view['Consumed'].plot()
plt.title('Average Energy Consumption')
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig('Energy used average.pdf', bbox_inches='tight')

plt.clf()
year_view['Generated'].plot()
plt.title('Average Energy Generation')
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig('Energy generated average.pdf', bbox_inches='tight')
