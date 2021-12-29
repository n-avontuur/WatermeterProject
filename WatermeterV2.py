#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os


global Counter
Counter = 0

DigitalPin = 1
#Openhab URL
OpenhabUrl = "http://192.168.0.227:8080"

#Open meterstand.txt file en lees meterstand
#Als meterstand.txt niet aanwezig is maakt script bestand aan en vult de meterstand
fn = "/home/pi/Documents/Scripts/meterstand_water.txt"
if os.path.exists(fn):
    f = file(fn, "r+")
    f = open(fn)
    inhoud = f.readline()
    a,b,c = inhoud.split()
    Counter = int(c)
else:
    f = open(fn, "w")
    f.write( 'meterstand = ' + repr(Counter))
    f.close()

#Board is pin nr, BMC is GPIO nr
#Read output from water meter op pin 40
GPIO.setmode(GPIO.BOARD)
# Set GPIO 21 (Pin 40) als Input aditioneel als Pullup-Weerstand aktiveren
GPIO.setup(DigitalPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def Interrupt(channel):
    print('Callback function called!')
    print('Callback function called!')
    time.sleep(0.05)         # need to filter out the false positive of some power fluctuation
    if GPIO.input(40) == 0:
       print('quitting event handler because this was probably a false positive')
       return
    #Teller elke interrupt uitlezen en met 0.5 liter verhogen (deler watermeter op 10 zetten)
    file(fn, "r+")
    f = open(fn)
    inhoud = f.readline()
    a,b,c = inhoud.split()
    Counter = int(c)
    Counter = Counter + 1
    f.close()
    #Schrijf meterstand naar bestand
    f = open( fn, 'w')
    f.write( 'meterstand = ' + repr(Counter))
    f.close()

def CallExistingTextFile():
    if os.path.exists(fn):
    f = file(fn, "r+")
    f = open(fn)
    inhoud = f.readline()
    a,b,c = inhoud.split()
    Counter = int(c)
    return (Counter)

def CreatNewTextFile():
    f = open(fn, "w")
    f.write( 'meterstand = ' + repr(Counter))
    f.close()