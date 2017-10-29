#import Libraries
import RPi.GPIO as GPIO
import time
import pyrebase
import Adafruit_DHT

#Firebase Configuration
config = {
  "apiKey": "ZWOpnNiFZBPRCGC7J2zyA9AXwaaCrF5x63PXvXPy",
  "authDomain": "https://temp-438dc.firebaseio.com/",
  "databaseURL": "https://temp-438dc.firebaseio.com/",
  "storageBucket": "https://temp-438dc.firebaseio.com/"
}
firebase_url = 'https://temp-438dc.firebaseio.com/'  
temperature_location = 'Taipei';  

firebase = pyrebase.initialize_app(config)

als = True
while als:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4) # gpio pin 4 or pin number 7
    if humidity is not None and temperature is not None:
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print (" Temperature = {0:0.1f}C  Humidity = {1:0.1f}% ".format(temperature, humidity))
    else:
        print ("can not connect to the sensor!")


result = requests.post(firebase_url + '/' + temperature_location + '/temperaturehumidity.json', data=json.dumps(data))  
print ("Status Code = ' + str(result.status_code) + ', Response = ' + result.text ")


time.sleep(1)
