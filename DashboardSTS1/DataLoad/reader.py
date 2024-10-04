import json
import csv
import socket
from datetime import datetime

class UDPSensorReader:
    def __init__(self, ip="0.0.0.0", port=50683, csv_file_path='udp_data.csv'):
        self.ip = ip
        self.port = port
        self.csv_file_path = csv_file_path
        self.headers = ["Timestamp", "Temperature (TMP112)", "Temperature (BME688)", "Humidity", "Pressure",
                        "Gas Resistance", "Acceleration X", "Acceleration Y", "Acceleration Z",
                        "Gyroscope X", "Gyroscope Y", "Gyroscope Z", "UVA", "UVA Index"]
        self.sock = None

    def start_listening(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
            print(f"Listening for UDP packets on {self.ip}:{self.port}")

            with open(self.csv_file_path, mode='a', newline='') as file:
                file_empty = file.tell() == 0
                writer = csv.writer(file)

                if file_empty:
                    writer.writerow(self.headers)

                while True:
                    data, addr = self.sock.recvfrom(1024)  # Buffer size
                    print(f"Data received from {addr}")
                    self.process_data(data, writer)

        except KeyboardInterrupt:
            print("\nListening stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.sock:
                self.sock.close()
            print("Socket closed.")

    def process_data(self, data, writer):
        try:
            decoded_data = data.decode()
            sensor_data = json.loads(decoded_data)
            print(f"Decoded Data: {sensor_data}")

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([current_time] + [sensor_data.get(key, '') for key in self.headers[1:]])
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
