#!/usr/bin/python
from typing import Literal
#GPIO library
import RPi.GPIO as GPIO
import time
import os

#Openhab library
from openhab import OpenHAB

global Counter
Counter = 0
DigitalPin = 40

#Setting up Openhab connection
OpenhabUrl = "http://192.168.0.228:8080/rest"
openhab = OpenHAB(OpenhabUrl) 
items = openhab.fetch_all_items()

#Open meterstand.txt file en lees meterstand
#Als meterstand.txt niet aanwezig is maakt script bestand aan en vult de meterstand
fn = "/home/pi/Documents/Scripts/meterstand_water.txt"

#Board is pin nr, BMC is GPIO nr
#Read output from water meter op pin 40
GPIO.setmode(GPIO.BOARD)
# Set GPIO 21 (Pin 40) als Input aditioneel als Pullup-Weerstand aktiveren
GPIO.setup(DigitalPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def CallExistingTextFile():
    f = file(fn, "r+")
    f = open(fn)
    inhoud = f.readline()
    a,b,c = inhoud.split()
    Counter = int(c)
    return (Counter, f)

def ReadTextFile():
    f = open(fn, "w")
    f.write('meterstand = ' + repr(Counter))
    f.close()

def Interrupt(channel):
    
    Liters = openhab.get_item('WatermeterM3')
    M3 = openhab.get_item('WatermeterL')

    print('Callback function called!')
    time.sleep(0.05)         # need to filter out the false positive of some power fluctuation
    if GPIO.input(40) == 0:
       print('quitting event handler because this was probably a false positive')
       return
    #Teller elke interrupt uitlezen en met 0.5 liter verhogen (deler watermeter op 10 zetten)
    Counter, f = CallExistingTextFile()
    Counter = Counter + 1
    f.close()
    #Schrijf meterstand naar bestand
    ReadTextFile()
    # voor debug => print waarde van watermeter
    print ("Watermeter Counter =" + str(Counter))
    Liters.command(Counter)
    M3Counter = Counter/1000
    M3.command(M3Counter)


#main script that will run
if os.path.exists(fn):
    Counter =CallExistingTextFile()
else:
    ReadTextFile()

GPIO.add_event_detect(40, GPIO.RISING, callback = Interrupt, bouncetime = 200)

#Loop that will run script
try:
    while True:
      time.sleep(0.2)        
except KeyboardInterrupt:
    GPIO.cleanup()
    print ("\nBye")