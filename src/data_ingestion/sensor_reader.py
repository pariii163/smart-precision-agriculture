import serial
import time


class SensorReader:
    def __init__(self, port: str, baud_rate: int = 9600):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = None

    def connect(self):
        """
        Establish serial connection to the sensor device.
        """
        self.connection = serial.Serial(self.port, self.baud_rate, timeout=1)
        time.sleep(2)  # wait for connection to stabilize

    def read_line(self):
        """
        Reads one line of sensor data from serial.
        Expected format (CSV):
        N,P,K,pH,temperature,humidity,moisture
        """
        if self.connection is None:
            raise ConnectionError("Sensor not connected")

        line = self.connection.readline().decode("utf-8").strip()
        return line
    
    def parse_sensor_line(self, line: str) -> dict:
        """
        Parses a CSV sensor line into a dictionary.
        Expected order:
        N,P,K,pH,temperature,humidity,moisture
        """
        values = line.split(",")

        if len(values) != 7:
            raise ValueError("Invalid sensor data format")

        return {
            "N": float(values[0]),
            "P": float(values[1]),
            "K": float(values[2]),
            "pH": float(values[3]),
            "temperature": float(values[4]),
            "humidity": float(values[5]),
            "moisture": float(values[6]),
        }


    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None


if __name__ == "__main__":
    print("Sensor Reader module ready")
