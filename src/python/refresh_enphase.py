#! /usr/bin/env python3

import base64
import http.client
import json
import os
import time

api_key = os.environ['API_KEY']
connect = os.environ['AUTH_CREDENTIALS']
auth = base64.b64encode(connect).decode("utf-8")

# Refresh token

with open('/var/lib/enphase/auth_tokens.json', 'r') as token_file:
    tokens = json.load(token_file)
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

conn = http.client.HTTPSConnection("api.enphaseenergy.com")
payload = ''
headers = {'Authorization': f'Basic {auth}'}
conn.request("POST", f"/oauth/token?grant_type=refresh_token&refresh_token={refresh_token}", payload, headers)
res = conn.getresponse()
data = res.read()

with open('/var/lib/enphase/auth_tokens.json', 'w') as token_file:
    token_file.write(data.decode("utf-8"))

# Persist systems file

payload = ''
headers = {
  'Authorization': f"Bearer {access_token}"
}

conn.request("GET", f"/api/v4/systems?key={api_key}", payload, headers)
res = conn.getresponse()
data = res.read()

with open('/var/lib/enphase/systems.json', 'w') as systems_file:
    systems_file.write(data.decode("utf-8"))

time.sleep(600)