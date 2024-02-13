#Sophia Hagen 
#API für Teststation Code 
#Version1


import board
import busio
import adafruit_ltr390 
from fastapi import FastAPI
import adafruit_dht
from Adafruit_BMP085 import BMP085



app = FastAPI()

@app.get("/")
def root():
    return {"Hello"}

@app.get("/uv")
def uv():
    i2c=busio.I2C(board.SCL, board.SDA)
    ltr = adafruit_ltr390.LTR390(i2c)
    return {"UV":ltr.uvs, "Ambient Light":ltr.light , "UV Index":ltr.uvi, "LUX": ltr.lux}

@app.get("/temp1")
def temp1():
    dhtDevice1 = adafruit_dht.DHT22(board.D2)
    temp_c = dhtDevice1.temperature
    humidity = dhtDevice1.humidity
    return{"Temperatur":temp_c , "Feuchtigkeit": humidity}

@app.get("/temp2")
def temp2():
    dhtDevice2 = adafruit_dht.DHT22(board.D3)
    temp_c = dhtDevice2.temperature
    humidity = dhtDevice2.humidity
    return{"Temperatur":temp_c , "Feuchtigkeit": humidity}

@app.get("/druck")
def druck():
    bmp = BMP085(0x77)
    pressure = bmp.readPressure()
    return{"Druck": pressure}