from src.digital_twin.twin_state import DigitalTwinState
from src.models.crop_recommendation import CropRecommendationModel
from src.data_ingestion.dataset_loader import load_csv_dataset
from src.data_ingestion.preprocessor import basic_preprocess
from src.decision_support.live_pipeline import LiveDecisionPipeline
import time

# Step 1: Train model (once)
df = load_csv_dataset("data/soil_datasets/sample_crop_data.csv")
df = basic_preprocess(df)

model = CropRecommendationModel()
model.train(df, target_column="crop")

# Step 2: Initialize Digital Twin
initial_twin = DigitalTwinState(
    nitrogen=90,
    phosphorus=42,
    potassium=43,
    ph=6.5,
    temperature=25,
    humidity=60,
    moisture=30
)

# Step 3: Create live decision pipeline
pipeline = LiveDecisionPipeline(
    twin_state=initial_twin,
    model=model
)

print("Starting live digital twin system (refactored)...\n")

# Step 4: Simulated sensor stream
simulated_sensor_stream = [
    {"moisture": 32, "temperature": 26},
    {"moisture": 35, "temperature": 27},
    {"moisture": 38, "temperature": 28}
]

for data in simulated_sensor_stream:
    twin_state, recommendation = pipeline.process_new_data(data)

    print("Updated Twin State:", twin_state)
    print("Recommended Crop:", recommendation)
    print("-" * 40)

    time.sleep(1)
