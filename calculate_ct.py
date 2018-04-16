#!/usr/bin/python3
#
from __future__ import division # needed for floating point division in python2
from sunrise import sun
from datetime import date,datetime,time,timedelta

ct_lookup = [2000, 2300, 2600, 2900, 3300, 3800, 4300, 4600, 4700, 4800, 4900, 5000, 5050, 5100, 5200, 5300, 5400, 5500, 5500, 5500]

def colortemp():
  s = sun()
  sunrise = datetime.combine(date.today(), s.sunrise(when=datetime.now()))
  solarnoon = datetime.combine(date.today(), s.solarnoon(when=datetime.now()))
  sunset = datetime.combine(date.today(), s.sunset(when=datetime.now()))

  if (datetime.now() - sunrise).seconds < 0 or (datetime.now() - sunrise).days < 0:
    #print("It is before sunrise")
    return "bluehour"

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
    return "bluehour"

if __name__ == "__main__":
    print(colortemp())
