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
PUL=16
DIR =12
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)

###Motor####



###Fenster erstellen###
root = Tk()
root.wm_title("Controll Unit")
root.config(background = "#FFFFFF")

rightFrame = Frame(root, width=500, height =800)
rightFrame.grid(row=100, column =200, padx=0, pady=3)

###Waning Fenster Netzteil muss ein sein###

## init sensor device ##
dhtDevice1 = adafruit_dht.DHT22(board.D2)
dhtDevice2 = adafruit_dht.DHT22(board.D3)

###Relay UV-Lampe###
PinUV=12
VersorgUV=4
GNDUV=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GNDUV, GPIO.OUT)
GPIO.setup(PinUV, GPIO.OUT)

##Temperatursensoren

##Temperatursensor oben 
def REFRTMP1():
    while TRUE:
        try:
            temp_c = dhtDevice1.temperature
            humidity = dhtDevice1.humidity
            tmplab1 = Label(buttonFrame,text="Temperatur: {:.1f} °C ".format(temp_c),bg = "#FFFFFF")
            tmplab1.grid(row=0, column=1)
            humlab1 = Label(buttonFrame,text="Feuchtigkeit: {} %".format(humidity),bg = "#FFFFFF")
            humlab1.grid(row=10, column=1)
        except RuntimeError as error:
            print(error.args[0])                                                                                                                                 
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice1.exit()
            raise error
        time.sleep(2.0)

##Temperatursensor unten 
def REFRTMP2():
    while TRUE:
        try:
            temp_c = dhtDevice2.temperature
            humidity = dhtDevice2.humidity
            tmplab2 = Label(buttonFrame,text="Temperatur: {:.1f} °C ".format(temp_c),bg = "#FFFFFF")
            tmplab2.grid(row=0, column=2)
            humlab2 = Label(buttonFrame,text="Feuchtigkeit: {} %".format(humidity),bg = "#FFFFFF")
            humlab2.grid(row=10, column=2)
        except RuntimeError as error:
            print(error.args[0])                                                                                                                                 
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice2.exit()
            raise error
        time.sleep(2.0)
        
###UV Lampe#####
def UVLampe():
    
    global boolUV
    
    print(boolUV)
    boolUV = not boolUV
    print(boolUV)
    
    if boolUV == True :
        
        GPIO.output(PinUV,GPIO.HIGH)
        btuv["text"]= "UV-Lampe aus"
        print("ein")
        
    else:
        
        GPIO.output(PinUV,GPIO.LOW)
        btuv["text"]= "UV-Lampe ein"
        print("aus")
        


###Netzteil ein aus #####
def Netzteil():
    
    global boolNetz
    print(boolNetz)
    boolNetz = not boolNetz
    print(boolNetz)
    
    if boolNetz == True :
        
        GPIO.output(SIG,GPIO.HIGH)
        btnt["text"]= "Netzgerät aus"
        print(boolNetz)
        
    else:
        GPIO.output(SIG,GPIO.LOW)
        btnt["text"]= "Netzgerät ein"
        print(boolNetz)
        

###LED Streifen ein aus
def LED():
    
    global boolLED
    
    print(boolLED)
    boolLED = not boolLED
    print(boolLED)
    
    pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    pixels.fill((0,0,0))
    
    if boolLED == True :
        
        pixels.fill((0,255,0))
        btled["text"]= "Leuchten aus"
        print(boolLED)
        
    else:
        
        pixels.fill((0,0,0))
        btled["text"]= "Leuchten ein"
        print(boolLED)
        



### Exit ###  
def exitProgram():
    print("Exit Button pressed")
    root.destroy()
    pixels = neopixel.NeoPixel(board.D21, 40, brightness =5)
    pixels.fill((0,0,0))
    GPIO.cleanup()
    
    
def ButMOT_click():
    t2 = threading.Thread(target= MOTstart)
    t2.start()
    
###Motor ein aus###
def MOTstart():
    
    global boolMotor
    
    print("W")
    print(boolMotor)
    
    boolMotor = not boolMotor  #setzt immer zum gegenteil, 
    print(boolMotor)
    
    
    if boolMotor==True:
        
        btmot["text"]= "Motor Aus"
        GPIO.output(DIR,GPIO.HIGH)
        
        for x in range(10100):  # illegaler Zähler - eventuell falsches signal darum funktioniert schritmotor noicht
            #eventuell Bibs verwenden / DC-Motor
            
            print("EIN")
            GPIO.output(PUL,GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PUL,GPIO.LOW)
            time.sleep(0.00001)
            
            if boolMotor == False:
                break
    else:
        
        btmot["text"]= "Motor EIN"
        GPIO.output(PUL,GPIO.LOW)
        print("Aus")
        
        
        
        
    
if __name__ == "__main__":
    
    t1 = threading.Thread(target=REFRTMP1)  ##threading Temperatursensor oben 
    
    t1.start()
    
    t3 = threading.Thread(target=REFRTMP2)  ##threading Temperatursensor unten 
    
    t3.start()

                          
    
###Program mit X schließen####
#alle GPIO solle cleanen


###Gui Fenster ####
buttonFrame = Frame(rightFrame)
buttonFrame.grid(row=0, column=0, padx=50,pady=3) 

###LED Streifen ein aus####
btled = Button(buttonFrame,text="Leuchten ein", bg = "#FFFFFF", width=15,command = LED)
btled.grid(row=10,column=0, padx=10,pady=3)

###Motor ein aus####
btmot = Button(buttonFrame,text="Motor ein", bg = "#FFFFFF", width=15, command=ButMOT_click)
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
