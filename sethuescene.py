#!/usr/bin/python3
#
# requires studioimagninaire
# 00:17:88:17:3F:E3 (Philips Lighting BV)
#
# Required first argument of which scene/color temp to set
# Optional second argument of the number of minutes to transition over
#
from phue import Bridge
import sys
from sunrise import sun
from datetime import date,datetime,time,timedelta

# Constants
names = ('Floor lamp', 'Wooden', 'Modern bulb', 'Modern post', 'Hue lightstrip plus 1')
scenes = {
        'goldenhour'    : ([254, 254, 249, 247, 254], [[0.4455, 0.4285], [0.5162, 0.4147], [0.4983, 0.4503], [0.4613, 0.4462], [0.4613, 0.4462]]),
        'sunset'    : ([254, 198, 207, 228, 209], [[0.61, 0.38], [0.5654, 0.4015], [0.51, 0.4148], [0.4977, 0.4514], [0.51, 0.4148]]),
        'deepsea'   : ([228, 183, 183, 248, 0], [[0.1897, 0.0647], [0.6736, 0.3221], [0.6736, 0.3221],[0.1968, 0.0678],]),
        'concentrate'   : ([254, 254, 254, 254, 200], [[0.4449,0.4066], [0.4449,0.4066], [0.4449,0.4066], [0.4449,0.4066], [0.4449,0.4066]]),
        'ski'       : ([254, 254, 254, 254, 177], [[0.3327, 0.3413], [0.3327, 0.3413], [0.3514, 0.3479], [0.3514, 0.3479], [0.3341, 0.4508]]),
        'bluehour'  : ([209, 209, 209, 209, 209], [[0.1742, 0.0533], [0.1742, 0.0533], [0.1751, 0.0546], [0.1742, 0.0533], [0.1742, 0.0533]]),
        'christmas' : ([209, 209, 209, 209, 209], [[0.6621, 0.3388], [0.6621, 0.3388], [0.6621, 0.3388], [0.214, 0.709], [0.214, 0.709]]),
        'twilight'  : ([177, 177, 177, 177, 177], [[0.2919, 0.2305], [0.2919, 0.2305], [0.4789, 0.3758], [0.3594, 0.2895], [0.2925, 0.2315]])
    }
ct_lookup = [2000, 2300, 2600, 2900, 3300, 3800, 4300, 4600, 4700, 4800, 4900, 5000, 5050, 5100, 5200, 5300, 5400, 5500, 5500, 5500]

# Function to calculate the color temperature based on the current date/time and location (default is Midland)
def colortemp():
  s = sun()
  sunrise = datetime.combine(date.today(), s.sunrise(when=datetime.now()))
  solarnoon = datetime.combine(date.today(), s.solarnoon(when=datetime.now()))
  sunset = datetime.combine(date.today(), s.sunset(when=datetime.now()))

  if (datetime.now() - sunrise).seconds < 0 or (datetime.now() - sunrise).days < 0:
    #print("It is before sunrise")
    return "2000"

  elif (datetime.now() - solarnoon).seconds < 0 or (datetime.now() - solarnoon).days < 0:
    #print("it is between sunrise and solar noon")
    percent = (datetime.now() - sunrise).seconds / (solarnoon - sunrise).seconds
    index = int(percent * 20)
    return str(ct_lookup[index])

  elif (datetime.now() - sunset).seconds < 0 or (datetime.now() - sunset).days < 0:
    #print("it is between solar noon and sunset")
    percent = (datetime.now() - solarnoon).seconds / (sunset - solarnoon).seconds
    index = int((1 - percent) * 20)

    return str(ct_lookup[index])

  else:
    #print("It is after sunset")
    return "2000"


# Main Code
if len(sys.argv) == 1:
    quit("Call as: " + sys.argv[0] + " <scenename|color temp> [transition time in minues]")

if len(sys.argv) > 2:
    xyTransitionTime = briTransitionTime = int(sys.argv[2]) * 600
else:
    xyTransitionTime = briTransitionTime = 4        # This is the hue default (0.4 seconds)

with open('/root/hue/bridgeip.txt', 'r') as f:
    bridgeIP = f.readline().strip()
b = Bridge(bridgeIP)

target = sys.argv[1]
if target == 'calculate':
    target = colortemp()

if target.isdigit():
    tempk = int(target)
    tempm = int(1000000/tempk)
    
    for i in range(0, len(names)):
        if not b.get_light(names[i], 'on'): # Change the color immediately if the light was off
            xyTransitionTime = 0
            b.set_light(names[i], 'on', True)
        b.set_light(names[i], 'ct', tempm, xyTransitionTime)
        b.set_light(names[i], 'bri', 254, briTransitionTime)

elif target == 'off':
    for i in range(0, len(names)):
        b.set_light(names[i], 'on', False)

else:
    brites = scenes[target][0]
    hues = scenes[target][1]
    
    for i in range(0, len(names)):
        print(names[i])
        if not b.get_light(names[i], 'on'): # Change the color immediately if the light was off
            xyTransitionTime = 0
            b.set_light(names[i], 'on', True)
        b.set_light(names[i], 'xy', hues[i], xyTransitionTime)
        b.set_light(names[i], 'bri', brites[i], briTransitionTime)

