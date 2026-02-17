from src.digital_twin.twin_state import DigitalTwinState
from src.models.crop_recommendation import CropRecommendationModel
from src.models.disease_detection import DiseaseDetectionModel
from src.data_ingestion.dataset_loader import load_csv_dataset
from src.data_ingestion.preprocessor import basic_preprocess
from src.decision_support.recommendation_engine import RecommendationEngine

# -------------------------
# Train crop recommendation model
# -------------------------
df = load_csv_dataset("data/soil_datasets/sample_crop_data.csv")
df = basic_preprocess(df)

crop_model = CropRecommendationModel()
crop_model.train(df, target_column="crop")

# -------------------------
# Train disease detection model
# -------------------------
disease_model = DiseaseDetectionModel()
X, y, class_names = disease_model.load_labeled_images(
    "data/image_datasets/train"
)

disease_model.build_cnn(num_classes=len(class_names))
disease_model.train(X, y, epochs=1, batch_size=1)

# -------------------------
# Create Digital Twin state
# -------------------------
twin_state = DigitalTwinState(
    nitrogen=90,
    phosphorus=42,
    potassium=43,
    ph=6.5,
    temperature=26,
    humidity=60,
    moisture=32
)

# -------------------------
# Load one image
# -------------------------
test_image = X[0]

# -------------------------
# Generate combined recommendation
# -------------------------
engine = RecommendationEngine(
    crop_model=crop_model,
    disease_model=disease_model,
    class_names=class_names
)

result = engine.generate_recommendation(twin_state, test_image)

print("\nFINAL SYSTEM OUTPUT")
print("-------------------")
for key, value in result.items():
    print(f"{key}: {value}")
