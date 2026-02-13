#! /usr/bin/env python3
import datetime
import json
import os

import pyemvue
from pyemvue.enums import Scale, Unit

CHUNK = 30
OVERLAP = 1
START = 720
END = 20

username = os.getenv('EMPORIA_USERNAME')
password = os.getenv('EMPORIA_PASSWORD')

vue = pyemvue.PyEmVue()
vue.login(username=username, password=password, token_storage_file='emporia_keys.json')

devices = vue.get_devices()

frame = []
for days_ago in range(END, START, CHUNK):
    start = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_ago)
    end = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_ago) + datetime.timedelta(
        days=CHUNK + OVERLAP)
    usage_over_time, start_time = vue.get_chart_usage(devices[0].channels[0], start, end, scale=Scale.HOUR.value,
                                                      unit=Unit.KWH.value)

    timestamp = int(start_time.timestamp())

for kwh in usage_over_time:
    if not kwh:
        kwh = 0
    for offset in [0, 900, 1800, 2700]:  # Spread out over 15 minutes to match Enphase data
        frame.append({'Timestamp': timestamp + offset, 'EV Charger': kwh / 4.0 * 1000})
    timestamp += 3600

with open('history_emporia.json', 'w') as outfile:
    outfile.write(json.dumps(frame))
