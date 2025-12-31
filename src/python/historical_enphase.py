#! /usr/bin/env python3

import datetime
import http.client
import json
import os
import time

dt = datetime.datetime(2025, 10, 15, 0, 0, 0)
start_time = dt

with open('/var/lib/enphase/auth_tokens.json', 'r') as token_file:
    tokens = json.load(token_file)
access_token = tokens['access_token']
api_key = os.environ['API_KEY']

with open('/var/lib/enphase/systems.json', 'r') as systems_file:
    systems = json.load(systems_file)

system_id = systems['systems'][0]['system_id']

while start_time.timestamp() < time.time():
    solar_data = {}
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    # start_time = int((datetime.datetime.now()-datetime.timedelta(days=6)).timestamp())
    end_ts = int((start_time + datetime.timedelta(days=1)).timestamp())
    start_ts = int(start_time.timestamp())

    conn.request("GET", f"/api/v4/systems/{system_id}/rgm_stats?key={api_key}&start_at={start_ts}&end_at={end_ts}",
                 payload, headers)
    try:
        res = conn.getresponse()
    except:
        breakpoint()
    data = res.read()

    result = json.loads(data.decode("utf-8"))

    for readout in result['intervals']:
        interval_end = str(readout['end_at'])
        power = readout['wh_del']
        if interval_end not in solar_data:
            solar_data[interval_end] = {'wh_generated': power}
        else:
            solar_data[interval_end].update({'wh_generated': power})

    conn.request("GET",
                 f"/api/v4/systems/{system_id}/telemetry/consumption_meter?key={api_key}&start_at={start_ts}&granularity=day",
                 payload, headers)
    try:
        res = conn.getresponse()
    except:
        breakpoint()
    data = res.read()

    result = json.loads(data.decode("utf-8"))
    for readout in result['intervals']:
        interval_end = str(readout['end_at'])
        power = readout['enwh']
        if interval_end not in solar_data:
            solar_data[interval_end] = {'wh_consumed': power}
        else:
            solar_data[interval_end].update({'wh_consumed': power})

    date_string = time.strftime('%Y-%m-%d', time.gmtime(start_ts))
    with open(file='/var/lib/enphase/' + date_string + '.json', mode='w') as day_file:
        json.dump(solar_data, day_file)
    print(f'Data for {date_string} written')
    start_time = start_time + datetime.timedelta(days=1)
    time.sleep(60)
