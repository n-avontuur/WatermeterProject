#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import urllib2
import os

#Watermeter stand (wordt alleen initeel gebruikt als er geen bestand meterstand_water.txt is)
global Counter
Counter = 0

#Domoticz URL
domoticz_url = "http://192.168.2.152:8080"
#Domoticz IDX van de water sensor (RFXMeter)
idx = 181

#Open meterstand.txt file en lees meterstand
#Als meterstand.txt niet aanwezig is maakt script bestand aan en vult de meterstand
fn = "/home/pi/domoticz/scripts/meterstand_water.txt"
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
GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Functie  callback
#Dit is de functie die aangeroepen wordt in de interrupt
def Interrupt(channel):
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
    #Send counter to domoticz JSON
    url1 = domoticz_url+'/json.htm?type=command&param=udevice&idx='+str(idx)+'&svalue='+str(Counter)
    req1 = urllib2.Request(url1)
    response1 = urllib2.urlopen(req1)
    #Voor debug => print voorbeeld van de JSON aanroep en/of de counter
    print ("JSON call =" + str(url1))
    print ("Watermeter Counter =" + str(Counter))

    #Interrupt-Event toevoegen, sensor geeft een 0 en en bij detectie een 1
#Bij detectie een 1 daarom check stijgende interrupt.
GPIO.add_event_detect(40, GPIO.RISING, callback = Interrupt, bouncetime = 200)

try:
    while True:
      time.sleep(0.2)        
except KeyboardInterrupt:
  GPIO.cleanup()
  print ("\nBye")