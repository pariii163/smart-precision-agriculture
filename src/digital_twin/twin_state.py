from dataclasses import dataclass


@dataclass
class DigitalTwinState:
    """
    Represents the current digital twin state of the farm/soil environment.
    """

    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    temperature: float
    humidity: float
    moisture: float

    def as_dict(self):
        """
        Returns the twin state as a dictionary.
        Useful for ML model inputs.
        """
        return {
            "N": self.nitrogen,
            "P": self.phosphorus,
            "K": self.potassium,
            "pH": self.ph,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "moisture": self.moisture
        }


if __name__ == "__main__":
    print("Digital Twin State module ready")
