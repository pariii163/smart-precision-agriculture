from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = "data/image_datasets/train"

datagen = ImageDataGenerator(rescale=1./255)

train_gen = datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(128, 128),
    batch_size=32,
    class_mode="binary"
)

print("Class indices mapping:")
print(train_gen.class_indices)
