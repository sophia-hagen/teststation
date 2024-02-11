###LEDs###
import board
import neopixel

###GPIO und TKinter###
from tkinter import *
import RPi.GPIO as GPIO
import sys

###Thread###
import threading 

## AM2302 ##
import time
import board
import adafruit_dht

###Warning Box ###
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as mbox


from time import sleep

###Variablne###
boolLED = False
boolNetz = False 
temp_c=0
boolMotor = False
boolUV = False

###Relay Netzteil###
NC= 14
SIG=15
GPIO.setmode(GPIO.BCM)
GPIO.setup(NC, GPIO.OUT)
GPIO.setup(SIG, GPIO.OUT)

#motor
PUL=1-6
DIR =12
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)



GPIO.output(DIR,GPIO.LOW)
for i in range(20000):  # illegaler Zähler - eventuell falsches signal darum funktioniert schritmotor noicht
            #eventuell Bibs verwenden / DC-Motor
            
            print("EIN")
            GPIO.output(PUL,GPIO.HIGH)
            time.sleep(0.00002)
            GPIO.output(PUL,GPIO.LOW)
            time.sleep(0.00002)
            
GPIO.output(DIR,GPIO.HIGH)           