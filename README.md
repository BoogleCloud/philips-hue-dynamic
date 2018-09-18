# Philips Hue Python Control Library
This builds off phue, a python wrapper for the REST API that hue offers (http://developer.hue.com). The main control binary is sethuescene.py which is designed to be run from a cron job.

The first argument is the scene to set. If this is a number we assume it is a color temperature in the range 2000-6500 and set it. If it is a phrase, we look for a scene matching the name and set those color values. If it is 'calculate' we calculate the color temperature for a given lat/long and the current date/time. This allows a dynamic setting of color temperature to match the progress of the sun.

The second argument is the number of minutes to transition up to 60.

## Setup
`apt install python3-setuptools python3-dev build-essential`\
`cd phue-master`\
`python3 setup.py install`

Set the IP address (or resolvable hostname) of your hue bridge in 'bridgeip.txt'

Now you can run the various python scripts.

## Future work
Expand to allow targeting of different zones and/or read the state of switches to determine if there is a manual override.
