#! /usr/bin/env python3

import json
import time

json_text = json.dumps({'time': time.time(),
                        'ctime': time.ctime()})

with open('/var/lib/enphase/test_token.json', 'w') as test_token:
    test_token.write(json_text)
