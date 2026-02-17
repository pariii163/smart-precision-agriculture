from src.digital_twin.twin_state import DigitalTwinState


def update_twin_state(current_state: DigitalTwinState, new_data: dict) -> DigitalTwinState:
    """
    Updates the digital twin state using new observed data.
    Simple overwrite strategy for now.
    """

    updated_state = DigitalTwinState(
        nitrogen=new_data.get("N", current_state.nitrogen),
        phosphorus=new_data.get("P", current_state.phosphorus),
        potassium=new_data.get("K", current_state.potassium),
        ph=new_data.get("pH", current_state.ph),
        temperature=new_data.get("temperature", current_state.temperature),
        humidity=new_data.get("humidity", current_state.humidity),
        moisture=new_data.get("moisture", current_state.moisture),
    )

    return updated_state


if __name__ == "__main__":
    print("Digital Twin update module ready")
