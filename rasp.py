#-*-coding:utf8-*-
"""
    Carriots.com
    Created 11 Jan 2013

    This sketch sends streams to Carriots according to the values read by a LDR sensor
"""
from light import *


import RPi.GPIO as GPIO
from urllib2 import urlopen, Request
from time import mktime, sleep
from datetime import datetime
from json import dumps
import os
import time

class Client (object):
    api_url = "http://api.carriots.com/streams"

    def __init__(self, api_key=None, client_type='json'):
        self.client_type = client_type
        self.api_key = api_key
        self.content_type = "application/vnd.carriots.api.v2+%s" % self.client_type
        self.headers = {'User-Agent': 'Raspberry-Carriots',
                        'Content-Type': self.content_type,
                        'Accept': self.content_type,
                        'Carriots.apikey': self.api_key}
        self.data = None
        self.response = None

    def send(self, data):
        self.data = dumps(data)
        request = Request(Client.api_url, self.data, self.headers)
        self.response = urlopen(request)
        return self.response




'''def execall():
    
    l=os.popen("python light.py")
    a=os.popen("python gyro.py")
    savedpath=os.getcwd()
    os.chdir("/sys/bus/w1/devices/28-0414645b8dff")
    t=open("w1_slave")
    print l.read()
    print a.read()
    print t.read()
    os.chdir(savedpath)'''
    


    
def main():
    GPIO.setmode(GPIO.BCM)

    on = 1  # Constant to indicate that lights are on
    off = 2  # Constant to indicate that lights are off

    device1 = "light@karthikkamathkr.karthikkamathkr"  # Replace with the id_developer of your device
    device2 = "temperature@karthikkamathkr.karthikkamathkr"  # Replace with the id_developer of your device
    device3 = "accelerometer@karthikkamathkr.karthikkamathkr"  # Replace with the id_developer of your device
    apikey = "6d9aa500b75c00d77079e69fb04e68c0941f4752173dbf2fa0458daf14eb3b0c"  # Replace with your Carriots apikey

    lights = off  # Current status

    client_carriots = Client(apikey)

    # The loop routine runs over and  over again forever
    while True:
        '''l=os.popen("python light.py")'''
        a=os.popen("python gyro.py")
        savedpath=os.getcwd()
        os.chdir("/sys/bus/w1/devices/28-0414645b8dff")
        t=open("w1_slave")
        '''print l.read()
        print a.read()'''
        temp=t.read()
        os.chdir(savedpath)
        timestamp = int(mktime(datetime.utcnow().timetuple()))
        li= float(readLight())
        te= float(temp[69:72])
        ac= a.read()
        print li
        if(li>1000):
            os.system('echo "light intensity is very high" | mail -s "light" meetcoolkarthik@gmail.com')
        data1 = {"protocol": "v2", "device": device1, "at": timestamp, "data": float(readLight())}
        carriots_response = client_carriots.send(data1)
        print carriots_response.read()
        print te
        if(te>280):
            os.system('echo "temperature is very high" | mail -s "temperature" meetcoolkarthik@gmail.com')
        data2 = {"protocol": "v2", "device": device2, "at": timestamp, "data": int(temp[69:72])}
        carriots_response = client_carriots.send(data2)
        print carriots_response.read()
        if '-' in ac:
            ac=ac[1:]
        print ac
        if(float(ac)>10):
            os.system('echo "box is not in right orientation" | mail -s "accelerometer" meetcoolkarthik@gmail.com')
        data3 = {"protocol": "v2", "device": device3, "at": timestamp, "data": float(ac)}
        carriots_response = client_carriots.send(data3)
        print carriots_response.read()
        
            


if __name__ == '__main__':
    main()
