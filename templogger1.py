import os
import sys
import urllib            # URL functions
import urllib2           # URL functions
import RPi.GPIO as GPIO  # GPIO library

import time #import time for creating delay 
import Adafruit_MAX31855.MAX31855 as MAX31855
import Adafruit_GPIO.SPI as SPI

# Raspberry Pi software SPI configuration.
CLK = 25
CS  = 24
DO  = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)

INTERVAL      = 1    # Delay between each reading (mins)
THINGSPEAKKEY = 'ABCDEFGH12345678'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

def sendData(url,key,field1,temp):
  """
  Send event to internet site
  """

  values = {'api_key' : key,'field1' : temp}


  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)
  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
  log = log + "{:.1f}C".format(temp) + "," ##LOOK

  try:
    # Send data to Thingspeak
    response = urllib2.urlopen(req, None, 5)
    html_string = response.read()
    response.close()
    log = log + 'Update ' + html_string
##  except urllib2.HTTPError, e:
##    log = log + 'Server could not fulfill the request. Error code: ' + e.code
##  except urllib2.URLError, e:
##    log = log + 'Failed to reach server. Reason: ' + e.reason
##  except:
##    log = log + 'Unknown error'

##  print (log)
    while 1:
        temperature = sensor.readTempC() 
        sendData(THINGSPEAKURL,THINGSPEAKKEY,'field1',temperature)
        sys.stdout.flush()
        time.sleep(30)

