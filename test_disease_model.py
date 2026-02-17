from src.models.disease_detection import DiseaseDetectionModel

# Initialize model
model = DiseaseDetectionModel()

# Load labeled images
X, y, class_names = model.load_labeled_images(
    "data/image_datasets/train"
)

print("Classes:", class_names)
print("Training samples:", len(X))

# Build CNN
model.build_cnn(num_classes=len(class_names))

# Train CNN (very few epochs, just to test pipeline)
model.train(X, y, epochs=2, batch_size=1)

# Test prediction on first image
prediction = model.predict(X[0])

print("Raw prediction:", prediction)
