from src.models.disease_detection import DiseaseDetectionModel

model = DiseaseDetectionModel()

image = model.load_image("data/image_datasets/train/sample_leaf.jpg")

print("Image loaded successfully")
print("Image shape:", image.shape)
print("Min pixel value:", image.min())
print("Max pixel value:", image.max())
