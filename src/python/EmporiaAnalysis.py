#! /usr/bin/env python3
import os

import matplotlib.pyplot as plt
import pandas as pd

enphase_directory = os.getenv('ENPHASE_DATA_DIRECTORY')

emporia_df = pd.read_feather(enphase_directory + '/' + 'emporia.ft')

tmp_view = emporia_df
tmp_view.drop('Date', axis=1, inplace=True)
year_view = tmp_view.groupby([(tmp_view.index.hour)]).mean()

plt.clf()
year_view['EV Charger'].plot()
plt.title('Average EV Charger Consumption')
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig('EV used average.pdf', bbox_inches='tight')

