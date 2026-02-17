from src.models.disease_detection import DiseaseDetectionModel

model = DiseaseDetectionModel()

X, y, class_names = model.load_labeled_images(
    "data/image_datasets/train"
)

print("Classes found:", class_names)
print("Number of images:", len(X))
print("Labels:", y)
print("Image shape:", X[0].shape if len(X) > 0 else "No images loaded")
