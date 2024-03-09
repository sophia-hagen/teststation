#Sophia Hagen 
#API für Teststation Code 
#Version1
#-----------------Postfach--------------------#
import socket

def start_tcp_server(host='0.0.0.0', port=1110):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"TCP Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                conn.sendall(data)  # Echo back the received data

if __name__ == '__main__':

    start_tcp_server()
#-----------------------------------------------------------------------#

#-------------Einbindungen-------------#
import board
import busio
import adafruit_ltr390 
from fastapi import FastAPI
import adafruit_dht
import bmp180
import RPi.GPIO as GPIO
#import neopixel
import time
#--------------------------------------#


app = FastAPI()

#---------Temperatur---------#
temp_c=0
humidity=0
#----------------------------#



#---------UV-Lampe---------#
boolUV = False
PinUV=12
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
GPIO.setup(filterPin, GPIO.OUT)
#--------------------------#

#---------Lüftung---------#
lueftungPin = 8
GPIO.setup(lueftungPin, GPIO.OUT)
boolLüftung = False
#--------------------------#

#--------------Temperatursensor---------------#
#GPIO.setup(D7, GPIO.OUT)
#GPIO.setup(D8, GPIO.OUT)
#---------------------------------------------#


#------------------------------------UV-Sensor-------------------------------------------------#
@app.get("/uv")
def uv():
    i2c = board.I2C()
    ltr = adafruit_ltr390.LTR390(i2c)

    while True:
        return("UV-Index:", ltr.uvi, "Umgebungslicht in Lux:", ltr.light)
        time.sleep(1.0)
#----------------------------------------------------------------------------------------------#



#------------------------------------Temp-Sensor-1---------------------------------------------#
@app.get("/temp1")
def temp1():
    dhtDevice1 = adafruit_dht.DHT22(board.D7)
    temp_c = dhtDevice1.temperature
    humidity = dhtDevice1.humidity
    return{"Temperatur in °C":temp_c , "Feuchtigkeit in %": humidity}
#----------------------------------------------------------------------------------------------#



#------------------------------------Temp-Sensor-2---------------------------------------------#
@app.get("/temp2")
def temp2():
    dhtDevice2 = adafruit_dht.DHT22(board.D8)
    temp_c = dhtDevice2.temperature
    humidity = dhtDevice2.humidity
    return{"Temperatur in °C":temp_c, "Feuchtigkeit in %": humidity + "%"}
#----------------------------------------------------------------------------------------------#



#------------------------------------Druck-Sensor---------------------------------------------#
@app.get("/druck")
def druck():
    i2c = board.I2C()
    bmp = bmp180.BMP180(i2c)
    bmp.sea_level_pressure = 1013.25
    return{f"Druck: {bmp.pressure:.1f} hPa", f"Meereshöhe: {bmp.altitude:.1f} Meter"} 
#----------------------------------------------------------------------------------------------#


#---------------------------------------UV-Lampe-----------------------------------------------#
@app.post("/uvlampe")
def uvlampe():
    global boolUV
    boolUV = not boolUV
    if boolUV == True :
        GPIO.output(PinUV,GPIO.HIGH)
        return{"UV-Lampe eingeschalten"}
    else:
        GPIO.output(PinUV,GPIO.LOW)
        return{"UV-Lampe ausgeschalten"}
#----------------------------------------------------------------------------------------------#



#---------------------------------------Netzteil-----------------------------------------------#
@app.post("/netzteil")
def netzteil():
    global boolNetz
    boolNetz = not boolNetz
    if boolNetz == True :
        GPIO.output(SIG,GPIO.HIGH)
        return{"Netzteil ausgeschalten"}
    else:
        GPIO.output(SIG,GPIO.LOW)
        return{"Netzteil eingeschalten"}
#----------------------------------------------------------------------------------------------#



#---------------------------------------LED-Streifen------------------------------------------#
@app.post("/led")
def ledstreifen():
    global boolLED
    boolLED = not boolLED
    pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    pixels.fill((0,0,0))
    if boolLED == True :
        pixels.fill((0,255,0))
        return{"LED-Streifen ausgeschalten"}
        
    else:
        
        pixels.fill((0,0,0))
        return{"LED-Streifen eingeschalten"}
#----------------------------------------------------------------------------------------------#
    


#---------------------------------------Motor------------------------------------------#
@app.post("/motor")
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
#----------------------------------------------------------------------------------------------#

#-------------------------------------------kühlung--------------------------------------------#
@app.post("/kühlung")
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
#----------------------------------------------------------------------------------------------#

#---------------------------------------Kühlung Aus--------------------------------------------#
@app.post("/kühlungaus")
def kuehlungaus():
    GPIO.output(motorPin,GPIO.LOW)
    GPIO.output(filterPin,GPIO.LOW)
    return{"Kühlung ausgeschalten"}
#----------------------------------------------------------------------------------------------#


#-------------------------------------------Lüftung--------------------------------------------#
@app.post("/lüftung")
def lueftung():
    global boolLüftung
    boolLüftung = not boolLüftung
    if boolLüftung==True:
        GPIO.output(lueftungPin,GPIO.HIGH)
        return{"Lüftung eingeschalten"}
    else:
        GPIO.output(lueftungPin,GPIO.LOW)
        return{"Lüftung ausgeschalten"}
#----------------------------------------------------------------------------------------------#