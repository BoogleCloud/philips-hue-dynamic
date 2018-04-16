#
# requires studioimagninaire
# 00:17:88:17:3F:E3 (Philips Lighting BV)
#
import sys
from phue import Bridge

with open('/root/hue/bridgeip.txt', 'r') as f:
	bridgeIP = f.readline().strip()

b = Bridge(bridgeIP)
lights = b.lights

print('# ' + sys.argv[1])

for l in lights:
	print(l.name)

for l in lights:
	print(l.brightness)
	
for l in lights:
    print(l.xy)
