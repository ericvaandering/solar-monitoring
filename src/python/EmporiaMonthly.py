#! /usr/bin/env python3
import datetime
import json
import os

import pyemvue
from pyemvue.enums import Scale, Unit

CHUNK = 8
OVERLAP = 1
START = 32
END = 0

username = os.getenv('EMPORIA_USERNAME')
password = os.getenv('EMPORIA_PASSWORD')


def print_recursive(usage_dict, info, depth=0):
    for gid, device in usage_dict.items():
        for channelnum, channel in device.channels.items():
            name = channel.name
            if name == 'Main':
                name = info[gid].device_name
            print('-' * depth, f'{gid} {channelnum} {name} {channel.usage} kwh')
            if channel.nested_devices:
                print_recursive(channel.nested_devices, info, depth + 1)


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
    # print(int(start_time.timestamp()))
    # print(usage_over_time)
    timestamp = int(start_time.timestamp())

    for kwh in usage_over_time:
        if not kwh:
            kwh = 0
        for offset in [0, 900, 1800, 2700]:  # Spread out over 15 minutes to match Enphase data
            frame.append({'Timestamp': timestamp + offset, 'EV Charger': kwh / 4.0 * 1000})
        timestamp += 3600
year = datetime.datetime.now(datetime.timezone.utc).year
month = datetime.datetime.now(datetime.timezone.utc).month

with open(f'{year}-{month:02d}_emporia.json', 'w') as outfile:
    outfile.write(json.dumps(frame))
