import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight

# ----------------------------
# Settings
# ----------------------------
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 5

TRAIN_DIR = "data/image_datasets/train"
TEST_DIR  = "data/image_datasets/test"

# ----------------------------
# Data Generators
# ----------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# ----------------------------
# Compute Class Weights
# ----------------------------
class_labels = train_gen.classes
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(class_labels),
    y=class_labels
)

class_weights_dict = {
    0: class_weights[0],
    1: class_weights[1]
}

print("Class Weights:", class_weights_dict)

# ----------------------------
# CNN Model
# ----------------------------
model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(128,128,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ----------------------------
# Train Model
# ----------------------------
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=test_gen,
    class_weight=class_weights_dict
)

# ----------------------------
# Save Model
# ----------------------------
os.makedirs("src/models", exist_ok=True)
model.save("src/models/plant_disease_cnn_baseline.h5")

print("\nModel saved to src/models/plant_disease_cnn_baseline.h5")
