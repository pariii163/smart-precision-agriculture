import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model(
    "src/models/plant_disease_cnn_baseline.h5"
)

# Path to test image (change filename as needed)
IMG_PATH = "data/image_datasets/test/healthy/ffd8d1a7-1596-4c8a-bd05-1e284b8cfaa5___JR_HL 8266.jpg"

# Load and preprocess image
img = image.load_img(IMG_PATH, target_size=(128, 128))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array)[0][0]

if prediction > 0.5:
    label = "Healthy"
    confidence = prediction
else:
    label = "Diseased"
    confidence = 1 - prediction

print("\nPrediction:", label)
print("Confidence:", round(float(confidence), 4))
