from gpiozero import PWMOutputDevice
from time import sleep

# Definiere den Motorpin (verwende GPIO13, entsprechend motorPin 13 im Arduino-Code)
motorPin = PWMOutputDevice(13)

def setup():
    # Initialisiere den Motorpin, in gpiozero nicht erforderlich, da bei der Instanziierung von PWMOutputDevice gemacht
    pass

def loop():
    # Geschwindigkeit muss eine Zahl zwischen 0 (aus) und 1 (volle Geschwindigkeit) sein
    speed = 1.0  # Ändere diesen Wert, um die Motorgeschwindigkeit zu steuern (0.0 bis 1.0)
    
    # Setze die Motorgeschwindigkeit
    motorPin.value = speed
    sleep(10)  # Läuft für 10 Sekunden bei dieser Geschwindigkeit

if _name_ == '_main_':
    setup()
    while True:
        loop()