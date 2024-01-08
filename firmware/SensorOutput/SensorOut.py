from STS1_Sensors import Sensors
import smbus2

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Create an instance of the Sensors class
sensors = Sensors(bus)

# Set up the sensors
sensors.setup()

# Get the sensor data
sensors.getData()

# Retrieve and print the sensor data
data = sensors.output
print("Temperature (TMP112):", data.tempTMP)
print("Temperature (BME688):", data.tempBME)
print("Humidity:", data.hum)
print("Pressure:", data.press)
print("Gas Resistance:", data.gasRes)
print("Acceleration X:", data.accX)
print("Acceleration Y:", data.accY)
print("Acceleration Z:", data.accZ)
print("Gyroscope X:", data.gX)
print("Gyroscope Y:", data.gY)
print("Gyroscope Z:", data.gZ)
print("UVA:", data.uva)
print("UVA Index:", data.uvaI)
# Add more print statements for other sensor data as needed
