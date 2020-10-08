import serial 
import requests
import httplib
import RPi.GPIO as GPIO
import time
import threading
import os

httpserv = ('http://192.168.0.251/ethernet/data.php')
tempread = serial.Serial('/dev/myUSB',9600)
relay = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay,GPIO.OUT)
GPIO.output(relay, GPIO.LOW)

def QR_Scan():

        try:
            barcode = raw_input('Scan:')
            if not barcode:
                print 'Scan Barcode First'
                pass
            temphex = tempread.read(6).encode('hex')
            tempval = int(temphex[4:8],16)
            if tempval <= 374:
                GPIO.output(relay, GPIO.HIGH)
                print "OPEN"
                time.sleep(5)
                GPIO.output(relay, GPIO.LOW)
                print "CLOSED"
            temperature = str(float(tempval)/10)
            print barcode
            print temperature
            r = requests.get(httpserv,params = barcode + temperature)
            print r.text
        except  (OSError,serial.serialutil.SerialException):
            print("No data")
            continue

while True:
    
    QR_Scan()

    
GPIO.cleanup()
