import RPi.GPIO as GPIO
import time
#huhu
# Pin-Nummern dem Broadcom SOC channel zuordnen
GPIO.setmode(GPIO.BCM)

# Pin 11 (GPIO17) als Ausgang initialisieren
motorPin = 17
GPIO.setup(motorPin, GPIO.OUT)

# Hauptprogramm
def main():
    try:
        # Setzt den Pin anfangs auf High
        GPIO.output(motorPin, GPIO.HIGH)
        time.sleep(2)  # Warte 2 Sekunden

        while True:
            # Setzt den Pin auf Low
            GPIO.output(motorPin, GPIO.LOW)
            time.sleep(0.1)  # Warte 100 ms
            # Setzt den Pin auf High
            GPIO.output(motorPin, GPIO.HIGH)
            time.sleep(5)  # Warte 5 Sekunden

    except KeyboardInterrupt:
        # Programm beenden, wenn ein KeyboardInterrupt auftritt
        GPIO.cleanup()  # Aufräumen
        
if _name_ == '_main_':
    main()