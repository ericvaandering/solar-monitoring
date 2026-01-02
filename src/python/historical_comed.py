#! /usr/bin/env python3

import datetime
import http.client
import json
import os
import sys
import time

DAYS_AGO = 4

days_ago = datetime.datetime.now() + datetime.timedelta(days=-DAYS_AGO)
dt = datetime.datetime(days_ago.year, days_ago.month, days_ago.day, 0, 0, 0)
start_time = dt

while start_time.timestamp() < time.time():
    price_data = {}
    conn = http.client.HTTPSConnection("hourlypricing.comed.com")
    payload = ''
    headers = ''


 # Returns list of [{"millisUTC":"1434686700000","price":"2.0"}
    end_ts = int((start_time + datetime.timedelta(days=1)).timestamp())
    start_ts = int(start_time.timestamp())
    (year, month, day, _, _, _, _, _, _) = start_time.timetuple()


    # url = f'https://hourlypricing.comed.com/api?type=5minutefeed&datestart={year}{month}{day}{hour}{minute}&dateend={year}{month}{day}{hour}{minute}'
    url = f'/api?type=5minutefeed&datestart={year}{month:02d}{day:02d}0000&dateend={year}{month:02d}{day:02d}2359'
    conn.request("GET", url)
    try:
        res = conn.getresponse()
    except:
        sys.exit()
    if res.status != 200:
        sys.exit()

    data = res.read()
    result = json.loads(data.decode("utf-8"))

    sum_15 = 0
    samples = 0
    for interval in result:
        seconds = int(int(interval['millisUTC'])/1000)
        if not seconds % 900:
            samples += 1
            sum_15 += float(interval['price'])
            avg_15 = sum_15 / samples
            sum_15 = 0
            samples = 0
            price_data[str(seconds)] = avg_15
        else:
            samples += 1
            sum_15 += float(interval['price'])

    #     interval_end = str(readout['end_at'])
    #     power = readout['wh_del']
    #     if interval_end not in solar_data:
    #         solar_data[interval_end] = {'wh_generated': power}
    #     else:
    #         solar_data[interval_end].update({'wh_generated': power})


    #date_string = time.strftime('%Y-%m-%d', time.gmtime(start_ts))
    with open(file=f'/var/lib/enphase/{year}-{month:02d}-{day:02d}_comed.json', mode='w') as day_file:
         json.dump(price_data, day_file)
    print(f'ComEd data for {year}-{month:02d}-{day:02d} written')
    start_time = start_time + datetime.timedelta(days=1)
    time.sleep(10)
