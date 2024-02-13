#Sophia Hagen 
#API für Teststation Code 
#Version1


#-------------Einbindungen-------------#
import board
import busio
import adafruit_ltr390 
from fastapi import FastAPI
import adafruit_dht
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import neopixel
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
GPIO.setup(PinUV, GPIO.OUT)
#--------------------------#



#---------Netzteil---------#
boolNetz = False 
SIG=15
GPIO.setup(SIG, GPIO.OUT)
#--------------------------#


#---------LED-streifen---------#
boolLED = False
#--------------------------#



#---------Motor---------#
boolMotor = False
PUL=16
DIR =12
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
#--------------------------#



#------------------------------------UV-Sensor-------------------------------------------------#
@app.get("/uv")
def uv():
    i2c=busio.I2C(board.SCL, board.SDA)
    ltr = adafruit_ltr390.LTR390(i2c)
    return {"UV":ltr.uvs, "Ambient Light":ltr.light , "UV Index":ltr.uvi, "LUX": ltr.lux}
#----------------------------------------------------------------------------------------------#



#------------------------------------Temp-Sensor-1---------------------------------------------#
@app.get("/temp1")
def temp1():
    dhtDevice1 = adafruit_dht.DHT22(board.D2)
    temp_c = dhtDevice1.temperature
    humidity = dhtDevice1.humidity
    return{"Temperatur":temp_c , "Feuchtigkeit": humidity}
#----------------------------------------------------------------------------------------------#



#------------------------------------Temp-Sensor-2---------------------------------------------#
@app.get("/temp2")
def temp2():
    dhtDevice2 = adafruit_dht.DHT22(board.D3)
    temp_c = dhtDevice2.temperature
    humidity = dhtDevice2.humidity
    return{"Temperatur":temp_c , "Feuchtigkeit": humidity}
#----------------------------------------------------------------------------------------------#



#------------------------------------Druck-Sensor---------------------------------------------#
@app.get("/druck")
def druck():
    bmp = BMP085(0x77)
    pressure = bmp.readPressure()
    return{"Druck": pressure}
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
    


@app.post("/motor")
def motor():
    global boolMotor
    boolMotor = not boolMotor
    if boolMotor==True:

        GPIO.output(DIR,GPIO.HIGH)

        for x in range(10100): 
            
            
            GPIO.output(PUL,GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PUL,GPIO.LOW)
            time.sleep(0.00001)
            return{"Motor ausgeschalten"}
            
            if boolMotor == False:
                break
    else:
        GPIO.output(PUL,GPIO.LOW)
        return{"Motor ausgeschalten"}