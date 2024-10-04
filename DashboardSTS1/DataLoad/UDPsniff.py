import json
import csv
import socket
from datetime import datetime

# UDP setup
udp_ip = "0.0.0.0"  #Jede IP-Adresse auf dem Port zuhören
udp_port = 50687 #Port muss gleich wie auf dem Raspi sein
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Code zeile wurde in Kap 2.4.1 erklärt
sock.bind((udp_ip, udp_port)) #IP und Port dem Socket zuweisen

# Pfad der CSV Datei
csv_file_path = 'C:\\Users\\Constantin\\Documents\\5BHEL\\Diplomarbeit\\DashboardSTS1\\udp_data.csv'

# Definition der Headers
headers = ["Timestamp", "Temperature (TMP112)", "Temperature (BME688)", "Humidity", "Pressure",
           "Gas Resistance", "Acceleration X", "Acceleration Y", "Acceleration Z",
           "Gyroscope X", "Gyroscope Y", "Gyroscope Z", "UVA", "UVA Index"]

print(f"Listening for UDP packets on {udp_ip}:{udp_port}")

try:
    #Öffnen der CSV-Datei im Modus a
    with open(csv_file_path, mode='a', newline='') as file:
        # Überprüft, ob die Datei leer ist
        file_empty = file.tell() == 0
        #Erstellen eines CSV wirter Objekts
        writer = csv.writer(file)

        if file_empty: #Falls die CSV Datei noch leer ist
            writer.writerow(headers) #Headers als in erste Reihe einfügen

        while True:
            data, addr = sock.recvfrom(1024)  # Buffer size
            print(f"Data received from {addr}")

            try:
                #Daten in einen String konveriten
                decoded_data = data.decode()
                #Daten für die Verarbeitung in ein JSON-Objet umwandeln
                sensor_data = json.loads(decoded_data)
                #Ausgabe der Dekoddierten daten
                print(f"Decoded Data: {sensor_data}")
                #Erzeugung eines Zeitstempels 
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # FÜr jeden Zeitstempel werden die Sensordaten eingefügt
                writer.writerow([current_time] + [sensor_data.get(key, '') for key in headers[1:]])
                #Buffer der Datei löschen, damit Daten sofort geschrieben werden
                file.flush()
            except json.JSONDecodeError as e: #Apprüfung von Fehlern der JSON-Dekodierung
                print(f"JSON Decode Error: {e}") #Ausgabe des Fehlers 
            except Exception as e: #Apprüfung für allgemeine Fehler
                print(f"Unexpected error: {e}") #Ausgabe der allgemeinen Fehler

except KeyboardInterrupt:
    print("\nScript terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    sock.close()
    print("Socket closed.")

