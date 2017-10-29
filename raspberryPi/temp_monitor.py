from subprocess import check_output
from re import findall
from time import sleep, strftime, time
from pyfcm import FCMNotification
import logging
import logging.handlers
import requests
import json
import Adafruit_DHT
import time

# send Notification
def sendNotification( temp ):
	push_service = FCMNotification(api_key="AAAAwcaNGIE:APA91bG8XH4WgdqS7akF0PYAuSPJ8G-9t-YmjaRNGxwKfRLPinSWf3ngFAseKVmn1Ge3kN9XogJOIGlA5EeRJneQb0_Q2-bXgIy3-UKp0OVG0dOOKcRD4CE3SXMvzHjpU5ajps3VRGtN")
	message_title = "Room Temperature"
	if temp > 23:
            message_body = "The Room Temperature is more then 23c"
        else:
            message_body = "The Room Temperature is less then 16c"
        result = push_service.notify_topic_subscribers(topic_name="RoomTemperature", message_title=message_title, message_body=message_body,sound=True)
	#print "sending Notification"
	#print volume
	return
   


# ------------ Read the temperature


def get_temp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    if humidity is not None and temperature is not None:
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print (temperature)
        print (humidity)
        print (" Temperature = {0:0.1f}C  Humidity = {1:0.1f}% ".format(temperature, humidity))
    else:
        print ("can not connect to the sensor!")
    return(temperature)


def get_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    humidity = round(humidity, 2)
    return(humidity)


# ------------ Logging

def write_log(temp, tempF):
    cpu_logger.info("{0}\t{1:.1f}\t{2:.2f}".format(strftime("%Y-%m-%d %H:%M:%S"), temp, tempF))

# ------------ Write to firebase

def write_firebase(temp, tempF):
    #now = int(time())
    now = 2017
    data = '{{"time":"{0}", "temperature":{1:.1f}, "humidity":{2:.2f}}}'.format(strftime("%Y-%m-%d %H:%M:%S"), temp, tempF)

    # write to temperatures (ongoing)
    firebasePut('temperatures/{:d}.json'.format(now), data)
    # write to current
    firebasePut('current.json'.format(now), data)

# ------------ Firebase calls

def firebasePut(path, data):
    requests.put(getFirebaseUrl(path), params=getFirebaseQueryParams(), data=data)

def getFirebaseQueryParams():
    return {'auth': config.get('auth')}

def getFirebaseUrl(path):
    return '{}/{}/{}'.format(config.get('base_url'), config.get('pi_name'), path)

# ------------ Log Setup

file_name = 'cpu_temp_log.tsv'
cpu_logger = logging.getLogger('CPU')
cpu_logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=200*1024, backupCount=5)
cpu_logger.addHandler(handler)

# ------------ Data setup

config = json.load(open("/home/pi/config.json"))

# ------------ Do the Work
temp = get_temp()
tempF = get_humidity()

write_log(temp, tempF)
write_firebase(temp, tempF)

# Notification temp
if (temp < 16) or (temp > 23):
    sendNotification(temp)
