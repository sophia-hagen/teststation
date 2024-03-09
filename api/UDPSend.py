from STS1_Sensors import Sensors
import smbus2
import json
import time
import socket
import board
import busio
import adafruit_ltr390 
#from fastapi import FastAPI
import adafruit_dht
import bmp180
import RPi.GPIO as GPIO
#import neopixel
import time
#do musch no die Libraries hinzufügen die du bruchsch für die sensoren


# UDP Configuration 
udp_ip = '172.20.10.3' #Zieladresse: Kann verändert werden 
udp_port = 50687 #Portnummer: Kann verändert werden 

# Konfiguration der Wartezeit 
t_sleep = 5 #Wartezeit: Kann verändert werden

# Flag Controlling für den Loop
running = True


#---------Temperatur---------#
temp_c=0
humidity=0
#----------------------------#



#---------UV-Lampe---------#
boolUV = False
PinUV=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PinUV, GPIO.OUT)
#--------------------------#



#---------Netzteil---------#
boolNetz = False 
SIG=15
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIG, GPIO.OUT)
#--------------------------#


#---------LED-streifen---------#
boolLED = False
#--------------------------#



#---------Motor---------#
boolMotor = False
PUL=13
DIR =17
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
#--------------------------#

#---------Kühlung---------#
motorPin = 12
GPIO.setup(DIR, GPIO.OUT)
boolkühlung = False
filterPin = 21 #led Gpio
GPIO.setup(filterPin, GPIO.OUT)
#--------------------------#

#---------Lüftung---------#
lueftungPin = 19
GPIO.setup(lueftungPin, GPIO.OUT)
boolLüftung = False
#--------------------------#

#--------------Temperatursensor---------------#
temppin1 = 7
temppin2 = 8
GPIO.setup(temppin1, GPIO.OUT)
GPIO.setup(temppin2, GPIO.OUT)
#---------------------------------------------#


try:
    while running:
       
	#do bitte die ganzen Funktionen für alle sensoren zum lesen der werte einbinden 
        
        print("Temperature (TMP112):", data.tempTMP) #
        print("Temperature (BME688):", data.tempBME)
        print("Humidity:", data.hum)
        print("Pressure:", data.press)
        print("Gas Resistance:", data.gasRes)
        print("Acceleration X:", data.accX)
        print("Acceleration Y:", data.accY)
        print("Acceleration Z:", data.accZ)
        print("Gyroscope X:", data.gX)
        print("Gyroscope Y:", data.gY)
        print("Gyroscope Z:", data.gZ)
        print("UVA:", data.uva)
        print("UVA Index:", data.uvaI)     
 	#do bitte die Beschreibung ändern und die varialbeln vo da Sensoren umöndern

        # Create a dictionary to store sensor data
        sensor_data = {
            "Temperature (TMP112)": data.tempTMP,
            "Temperature (BME688)": data.tempBME,
            "Humidity": data.hum,
            "Pressure": data.press,
            "Gas Resistance": data.gasRes,
            "Acceleration X": data.accX,
            "Acceleration Y": data.accY,
            "Acceleration Z": data.accZ,
            "Gyroscope X": data.gX,
            "Gyroscope Y": data.gY,
            "Gyroscope Z": data.gZ,
            "UVA": data.uva,
            "UVA Index": data.uvaI
        } #do bitte die Beschreibung ändern und die varialbeln vo da Sensoren umöndern

        # Die Anreihung der Daten in eine JSON Datei umwandeln
        data_string = json.dumps(sensor_data)

        # UDP-Socket erstellen und öffnen
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Daten über UDP Socket schicken
        sock.sendto(data_string.encode(), (udp_ip, udp_port))

        sock.close()
        print(data_string)

        #Warten für t_sleep sekunden
        time.sleep(t_sleep)

except KeyboardInterrupt:
    # Programm Stopt sobald strg+c gedrückt wird
    running = False
    print("Loop stopped by user.")
