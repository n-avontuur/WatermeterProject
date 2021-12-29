#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import urllib2
import os

global Counter
Counter = 0

#Openhab URL
OpenhabUrl = "http://192.168.0.227:8080"

#Open meterstand.txt file en lees meterstand
#Als meterstand.txt niet aanwezig is maakt script bestand aan en vult de meterstand
fn = "/home/pi/Documents/Scripts/meterstand_water.txt"