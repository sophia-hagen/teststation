import board
import busio
import adafruit_ltr390

i2c=busio.I2C(board.SCL, board.SDA)

ltr = adafruit_ltr390.LTR390(i2c)

print("UV:", ltr.uvs, "\t\tAmbient Light:" , ltr.light)
print("UVI:", ltr.uvi, "\t\tLux:" , ltr.lux)