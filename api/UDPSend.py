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

#------------UV-Sensor------------#
def uv():
    i2c = board.I2C()
    ltr = adafruit_ltr390.LTR390(i2c)

    while True:
        return("UV-Index:", ltr.uvi, "Umgebungslicht in Lux:", ltr.light)
        time.sleep(1.0)
#------------------------------------#
        
#------------Temperatursensor 1------------#
def temp1():
    dhtDevice1 = adafruit_dht.DHT22(board.D26)
    temp_c = dhtDevice1.temperature
    humidity = dhtDevice1.humidity
    return{"Temperatur in °C":temp_c , "Feuchtigkeit in %": humidity}
#------------------------------------#

#------------Temperatursensor 2------------#
def temp2():
    dhtDevice2 = adafruit_dht.DHT22(board.D24)
    temp_c = dhtDevice2.temperature
    humidity = dhtDevice2.humidity
    return{"Temperatur in °C":temp_c, "Feuchtigkeit in %": humidity + "%"}
#------------------------------------#

#------------Drucksensor------------#
def druck():
    i2c = board.I2C()
    bmp = bmp180.BMP180(i2c)
    bmp.sea_level_pressure = 1013.25
    return{f"Druck: {bmp.pressure:.1f} hPa", f"Meereshöhe: {bmp.altitude:.1f} Meter"} 
#------------------------------------#

#------------UV-Lampe------------#
def uvlampe():
    global boolUV
    boolUV = not boolUV
    if boolUV == True :
        GPIO.output(PinUV,GPIO.HIGH)
        return{"UV-Lampe eingeschalten"}
    else:
        GPIO.output(PinUV,GPIO.LOW)
        return{"UV-Lampe ausgeschalten"}
#------------------------------------#
    
#------------Netzteil------------#
def netzteil():
    global boolNetz
    boolNetz = not boolNetz
    if boolNetz == True :
        GPIO.output(SIG,GPIO.HIGH)
        return{"Netzteil ausgeschalten"}
    else:
        GPIO.output(SIG,GPIO.LOW)
        return{"Netzteil eingeschalten"}
#------------------------------------#

#------------LED-Streifen------------#

#------------------------------------#
    
#------------Motor------------#
def motor():
    global boolMotor
    boolMotor = not boolMotor
    if boolMotor==True:

        GPIO.output(DIR,GPIO.HIGH)

        for x in range(10100): 
            
            GPIO.output(PUL,GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(PUL,GPIO.HIGH)
            time.sleep(0.5)
            return{"Motor eingeschalten"}
            
            #if boolMotor == False:
                #break
    else:
        GPIO.output(PUL,GPIO.LOW)
        return{"Motor ausgeschalten"}
#------------------------------------#
    
#------------Kühlung------------#
def kuehlung():
    global boolkühlung
    boolkühlung = not boolkühlung
    if boolkühlung==True:

        GPIO.output(motorPin,GPIO.HIGH)
        GPIO.output(filterPin,GPIO.HIGH)
        return{"Kühlung eingeschalten - Stuffe 1"}	
        time.sleep(2)  # Warte 2 Sekunden
     

    else:
        GPIO.output(motorPin,GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(motorPin,GPIO.HIGH)
        GPIO.output(filterPin,GPIO.HIGH)
        time.sleep(5)
        return{"Kühlung eingeschalten - Stuffe 2"}
#------------------------------------#

#---------------Kühlung AUS----------#
def kuehlungaus():
    GPIO.output(motorPin,GPIO.LOW)
    GPIO.output(filterPin,GPIO.LOW)
    return{"Kühlung ausgeschalten"}
#-----------------------------------#

#-------------------Lüftung-----------#
def lueftung():
    global boolLüftung
    boolLüftung = not boolLüftung
    if boolLüftung==True:
        GPIO.output(lueftungPin,GPIO.HIGH)
        return{"Lüftung eingeschalten"}
    else:
        GPIO.output(lueftungPin,GPIO.LOW)
        return{"Lüftung ausgeschalten"}
#----------------------------------------#



try:
    while running:
       
        Temperatur1 = temp1()
        Temperatur2 = temp2()
        UVsensor = uv()
        Drucksensor = druck()
        Uvlampe = uvlampe()
        Motor = motor()
        Kuehlung = kuehlung()
        kuelungAUS = kuehlungaus()
        Lueftung = lueftung()
        Netzteil = netzteil()
    
	#do bitte die ganzen Funktionen für alle sensoren zum lesen der werte einbinden 
        
        print("Temperaturesensor 1:", data.temp_c) #
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
