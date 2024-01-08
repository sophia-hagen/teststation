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
count =0
countnt =0
temp_c=0

###Relay Netzteil###
NC= 14
SIG=15
GPIO.setmode(GPIO.BCM)
GPIO.setup(NC, GPIO.OUT)
GPIO.setup(SIG, GPIO.OUT)

###Fenster erstellen###
root = Tk()
root.wm_title("Controll Unit")
root.config(background = "#FFFFFF")

rightFrame = Frame(root, width=500, height =800)
rightFrame.grid(row=100, column =200, padx=0, pady=3)

###Waning Fenster Netzteil muss ein sein###

## init sensor device ##
dhtDevice = adafruit_dht.DHT22(board.D4)


##Temperatursensor
def REFRTMP():
    while TRUE:
        try:
            temp_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            tmplab = Label(buttonFrame,text="Temperatur: {:.1f} °C ".format(temp_c),bg = "#FFFFFF")
            tmplab.grid(row=0, column=1)
            humlab = Label(buttonFrame,text="Feuchtigkeit: {} %".format(humidity),bg = "#FFFFFF")
            humlab.grid(row=10, column=1)
        except RuntimeError as error:
            print(error.args[0])                                                                                                                                 
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        time.sleep(2.0)


###Netzteil ein aus #####
def Netzteil():
    global countnt
    countnt += 2
    if countnt &2 == 0 :
        
        GPIO.output(SIG,GPIO.LOW)
        btnt["text"]= "Netzgerät EIN"
        print(countnt)
    else:
        
        GPIO.output(SIG,GPIO.HIGH)
        btnt["text"]= "Netzgerät AUS"
        print(countnt)

###LED Streifen ein aus
def LED():
    global count
    count += 2
    pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    pixels.fill((0,0,0))
    if count &2 == 0 :
        pixels.fill((0,0,0))
        btled["text"]= "Leuchten EIN"
        print(count)
    else:
        pixels.fill((0,255,0))
        btled["text"]= "Leuchten AUS"
        print(count)



### Exit ###  
def exitProgram():
    print("Exit Button pressed")
    root.destroy()
    pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    pixels.fill((0,0,0))
    GPIO.cleanup()
    

###Motor ein aus###
def MOTstart():
    
    print("W")
    
    for i in range(10):
        print("H")
        time.sleep(2.0)
  

def MOT_click(): ##hallo
    t2 = threading.Thread(target=MOTstart)  ##threading Motor
    
    t2.start()
    
    
    
##thread
if __name__ == "__main__":
    
    t1 = threading.Thread(target=REFRTMP)  ##threading Temperatursensor
    
    t1.start()
    

    
    
###Program mit X schließen####
#alle GPIO solle cleanen


###Gui Fenster ####
buttonFrame = Frame(rightFrame)
buttonFrame.grid(row=0, column=0, padx=50,pady=3) 

###LED Streifen ein aus####
btled = Button(buttonFrame,text="Leuchten ein", bg = "#FFFFFF", width=15,command = LED)
btled.grid(row=10,column=0, padx=10,pady=3)

###Motor ein aus####
btmot = Button(buttonFrame,text="Motor ein", bg = "#FFFFFF", width=15, command=MOT_click)
btmot.grid(row=20,column=0, padx=10,pady=3)


###Button Exit ####
btexit = Button(buttonFrame, text="Exit", bg = "#FF0000", width=15,command=exitProgram)
btexit.grid(row=50, column=1, padx=0,pady=5)

###Button Netzteil ein aus####
btnt= Button(buttonFrame, text="Netzteil ein", bg = "#FFFFFF", width=15,command = Netzteil)
btnt.grid(row=0, column=0)

###Button UV-Lampe####
btuv= Button(buttonFrame, text="UV-Lampe ein", bg = "#FFFFFF", width=15,command = UVLampe)
btuv.grid(row=20, column=1)


root.mainloop();
