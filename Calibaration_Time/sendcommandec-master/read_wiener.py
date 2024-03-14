#!/usr/bin/env python3

from urllib.request import urlopen
import pandas as pd

wiener_id  = "sbgps22"
wiener_url = "http://" + wiener_id + ".in2p3.fr"

wiener_web_page = pd.read_html(urlopen(wiener_url).read())

wiener_status = wiener_web_page[1]

global_power = wiener_status.values[0][1]

if global_power == 'ON':
    print(wiener_web_page[2])
else:
    print(wiener_status)
