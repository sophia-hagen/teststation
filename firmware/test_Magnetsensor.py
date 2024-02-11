import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

adc=Adafruit_ADS1x15.ADS1115()

GPIO .setmode(GPIO.BCM)
GPIO.setwarning(False)
GAIN = 1

delayTime = 1
Digital_pin = 23

GPIO.setup(Digital_pin, GPIO.IN, pull_up_down = GPIO.PUD_OFF)

while True:
    value = adc.read_adc(0, gain=GAIN)
    voltage = ((value/32767)*4096)/1000
    
    if GPIO.input(Digital_pin) == False:
        print("Spannungswert:", round(voltage,3),"V", "Grenzwert nicht erreicht")
    else:
        print("Spannungswert:", round(voltage,3),"V", "Grenzwert erreicht")
    print("--------------------------------------------------------------------")
    time.sleep(delayTime)