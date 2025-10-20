#! /usr/bin/env python3

import datetime
import http.client
import json
import os
import pprint
import time

with open('auth_tokens.json', 'r') as token_file:
  tokens = json.load(token_file)
access_token = tokens['access_token']
api_key = os.environ['API_KEY']

with open('systems.json', 'r') as systems_file:
  systems = json.load(systems_file)

system_id = systems['systems'][0]['system_id']

conn = http.client.HTTPSConnection("api.enphaseenergy.com")
payload = ''
headers = {
  'Authorization': f"Bearer {access_token}"
}

start_time = int((datetime.datetime.now()-datetime.timedelta(days=6)).timestamp())
end_time = int(time.time())

conn.request("GET", f"/api/v4/systems/{system_id}/rgm_stats?key={api_key}&start_at={start_time}&end_at={end_time}", payload, headers)
res = conn.getresponse()
data = res.read()

result = json.loads(data.decode("utf-8"))
pprint.pprint(result)

conn.request("GET", f"/api/v4/systems/{system_id}/telemetry/consumption_meter?key={api_key}&start_at={start_time}&granularity=day", payload, headers)
res = conn.getresponse()
data = res.read()

result = json.loads(data.decode("utf-8"))
pprint.pprint(result)
