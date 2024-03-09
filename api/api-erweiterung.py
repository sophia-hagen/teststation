import paho.mqtt.client as mqtt
import socket
import RPi.GPIO as GPIO
import board
import busio
import adafruit_dht
import adafruit_ltr390
import bmp180
import time
from threading import Thread



# MQTT Konfiguration
MQTT_BROKER = '192.168.250.150' #Host adresse
MQTT_PORT = 1883

# UDP Configuration für Sensor Daten
UDP_IP = "192.168.250.150" #Destinations Adresse
UDP_PORT = 50687
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Temperatur
temp_c = 0
humidity = 0 

# GPIO Setup
GPIO.setmode(GPIO.BCM)
PinUV = 12 #Pin für UV lampe 
SIG = 15 #Pin für Netzteil
PUL = 13 #Pin für motor 
DIR = 17 #Pin für Motor
LD = 14 #Pin für LEDs bitte Ändern
KLG = 16 #Pin für Kühlung bitte Ändern
motorPIN = 12 # Pin für die Kühlung?
lueftungPin = 1 # Pin für die Lüfter

GPIO.setup(PinUV, GPIO.OUT)
GPIO.setup(SIG, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(LD, GPIO.OUT)
GPIO.setup(KLG, GPIO.OUT)
GPIO.setup(lueftungPin, GPIO.OUT)

# Initialize I2C sensors





# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/actuators/control/#")

# Message Encoder
def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    if topic == '/actuators/control/uvlamp':
        control_uv_lamp(message)
    elif topic == 'home/actuators/control/netzteil':
        control_netzteil(message)
    elif topic == '/actuators/control/led':
        control_led(message)
    elif topic == '/actuators/control/motor':
        control_motor(message)
    elif topic == '/actuators/control/kuehlung':
        control_kuehlung(message)

# Funktionwen um Aktorik zu steuern 
def control_uv_lamp(command):
    if command == 'ON' :
        GPIO.output(PinUV,GPIO.HIGH)
        return{"UV-Lampe eingeschalten"}
    else:
        GPIO.output(PinUV,GPIO.LOW)
        return{"UV-Lampe ausgeschalten"}

def control_netzteil(command):
   if command == 'ON':
        GPIO.output(SIG,GPIO.HIGH)
        return{"Netzteil ausgeschalten"}
   else:
        GPIO.output(SIG, GPIO.LOW)
        return{"Netzteil eingeschalten"}
  
def control_led(command):
    # pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    # pixels.fill((0,0,0))
    # if command == 'ON' :
    #     pixels.fill((0,0,0))
    #     return{"LED-Streifen eingeschalten"}
    # else:
    #     pixels.fill((0,255,0))
    #     return{"LED-Streifen ausgeschalten"}
    pass
        
def control_motor(command):
    if command== "ON":
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
    
    
def control_kuehlung(command): #todo: Mehrere stunfen do isch nur stufe 1 dinna grad
    if command == 'ON':
        GPIO.output(motorPIN, GPIO.HIGH) #wieso motor pin?
        return{"Kühlung eingeschaltet "}
        time.sleep(2) #kritisch
    else:
        GPIO.output(motorPIN,GPIO.LOW)
        return{"Kühlung ausgeschalten"} 


def lueftung(command):
    if command == 'ON':
        GPIO.output(lueftungPin,GPIO.HIGH)
        return{"Lüftung eingeschalten"}
    else:
        GPIO.output(lueftungPin,GPIO.LOW)
        return{"Lüftung ausgeschalten"} 


#Sensordaten Funktionen
def druck():
    i2c = board.I2C()
    bmp = bmp180.BMP180(i2c)
    bmp.sea_level_pressure = 1013.25
    return{f"Druck: {bmp.pressure:.1f} hPa", f"Meereshöhe: {bmp.altitude:.1f} Meter"}
def temp2():
    dhtDevice2 = adafruit_dht.DHT22(board.D2)
    temp_c = dhtDevice2.temperature
    humidity = dhtDevice2.humidity
    return{"Temperatur in °C":temp_c, "Feuchtigkeit in %": humidity + "%"}
def temp1():
    dhtDevice1 = adafruit_dht.DHT22(board.D3)
    temp_c = dhtDevice1.temperature
    humidity = dhtDevice1.humidity
    return{"Temperatur in °C":temp_c , "Feuchtigkeit in %": humidity}
def uv():
    i2c = board.I2C()
    ltr = adafruit_ltr390.LTR390(i2c)

    while True:
        return("UV-Index:", ltr.uvi, "Umgebungslicht in Lux:", ltr.light)
    


# Sensor Data Sending Function
def send_sensor_data():
    while True:
    # Daten von jedem sensor ablesen
        pressure_data = druck()
        temp1_data = temp1()
        temp2_data = temp2()
        uv_data = uv()

    # Daten in einen String schreiben
        msg = f"{pressure_data}, {temp1_data}, {temp2_data}, {uv_data}"

    #  Daten über UDP senden
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    # 5 Sekunden warten bis zum nächsten Senden 
        time.sleep(5)


 
if __name__ == "__main__":
    # MQTT Client Setup
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # neue version von MQTT
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
 
    # Start MQTT Loop in a Thread
    mqtt_thread = Thread(target=client.loop_forever)
    mqtt_thread.start()
 

    # Start Sending Sensor Data in a Thread
    #sensor_data_thread = Thread(target=send_sensor_data)
    #sensor_data_thread.start()
