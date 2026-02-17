from src.digital_twin.twin_state import DigitalTwinState
from src.digital_twin.twin_update import update_twin_state

# Initial twin state
twin = DigitalTwinState(
    nitrogen=90,
    phosphorus=40,
    potassium=45,
    ph=6.5,
    temperature=25,
    humidity=60,
    moisture=30
)

print("Initial Twin State:")
print(twin)

# New incoming data (simulating sensor or dataset update)
new_data = {
    "moisture": 35,
    "temperature": 26
}

# Update twin
updated_twin = update_twin_state(twin, new_data)

print("\nUpdated Twin State:")
print(updated_twin)
