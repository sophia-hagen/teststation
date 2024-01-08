import STS1_Sensors as Sensors
from time import sleep

for i in range(1,7):
    sen = Sensors.SensorsData()
    print(sen)
    sleep(1)