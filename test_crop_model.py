import pandas as pd
from src.models.crop_recommendation import CropRecommendationModel
from src.data_ingestion.dataset_loader import load_csv_dataset
from src.data_ingestion.preprocessor import basic_preprocess
from src.digital_twin.twin_state import DigitalTwinState

# Load and preprocess dataset
df = load_csv_dataset("data/soil_datasets/sample_crop_data.csv")
df = basic_preprocess(df)

# Train model
model = CropRecommendationModel()
model.train(df, target_column="crop")

# Create a Digital Twin state (simulating live system state)
twin_state = DigitalTwinState(
    nitrogen=88,
    phosphorus=41,
    potassium=42,
    ph=6.6,
    temperature=25,
    humidity=59,
    moisture=32
)

# Predict crop from Digital Twin
prediction = model.predict_from_twin(twin_state)

print("Predicted crop from Digital Twin state:", prediction)
