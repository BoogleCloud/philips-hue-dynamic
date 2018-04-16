#!/usr/bin/python3
#
# requires studioimagninaire
# 00:17:88:17:3F:E3 (Philips Lighting BV)
#
from phue import Bridge
import sys

with open('/root/hue/bridgeip.txt', 'r') as f:
	bridgeIP = f.readline().strip()

b = Bridge(bridgeIP)

b.set_group('Office','on', False)
