import pandas as pd
import threading
import time

class LiveDataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.DataFrame()
        self.lock = threading.Lock()
        self.running = True  # Flag to control the background thread
        self.update_data()

    def read_csv_file(self):
        try:
            df = pd.read_csv(self.file_path)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')  # Coerce errors
            return df
        except Exception as e:
            print(f"Error reading file {self.file_path}: {e}")
            return pd.DataFrame()

    def update_data(self):
        with self.lock:
            self.data = self.read_csv_file()

    def get_latest_data(self):
        with self.lock:
            return self.data

    def start_loading(self):
        def load_data():
            while self.running:
                self.update_data()
                time.sleep(1)

        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()

    def stop_loading(self):
        """Stops the background data loading process."""
        self.running = False

# Usage
# loader = LiveDataLoader('path_to_csv')
# loader.start_loading()
# ... Use the loader ...
# loader.stop_loading()  # When you need to stop the thread
